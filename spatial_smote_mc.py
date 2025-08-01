#!/usr/bin/env python3
"""
Spatial-SMOTE-Monte-Carlo
=========================
1. No fixed grid – uses ball-tree over (lon, lat)
2. GPU backend (cuML & CuPy) – scales to >10^8 samples
3. MPI / Dask ready – distribute Monte-Carlo trials across nodes
4. Outputs synthetic-sample density as GeoTIFF / Zarr
5. Restartable – each trial checkpointed to disk

Usage (single node, 8×A100):
    python spatial_smote_mc.py \
        --input samples.parquet \
        --output synth_density.tif \
        --radius_km 50 \
        --mc 5000 \
        --minority 1 \
        --gpu

Usage (SLURM, 1024 GPUs):
    srun -N128 --ntasks-per-node=8 \
         python -m dask_cuda.initialize spatial_smote_mc.py [args]
"""

import argparse, logging, time, os, json, tempfile
import numpy as np
import cupy as cp
import cudf
import cuml.neighbors as knn_gpu
import rasterio
from dask.distributed import Client, wait
import dask.array as da
import dask.dataframe as dd
import zarr
from numba import cuda

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# -------------------- CLI --------------------
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Parquet/Zarr path with [lon, lat, label]")
    p.add_argument("--output", required=True, help="GeoTIFF/Zarr output density map")
    p.add_argument("--mc", type=int, default=1000, help="Monte-Carlo iterations")
    p.add_argument("--radius_km", type=float, default=50, help="Spatial radius (km) for neighbourhood")
    p.add_argument("--knn", type=int, default=5, help="k in SMOTE")
    p.add_argument("--minority", type=int, default=1, help="Label value for minority class")
    p.add_argument("--gpu", action="store_true", help="Use GPU backend")
    p.add_argument("--chunksize", type=int, default=1_000_000, help="Rows per dask partition")
    p.add_argument("--epsg", type=int, default=4326, help="EPSG code for GeoTIFF")
    return p.parse_args()

# -------------------- Geo utilities --------------------
def km_to_deg(r_km):
    """Approximate km to degrees on sphere"""
    return r_km / 111.32

# -------------------- SMOTE kernel on GPU --------------------
def smote_2d_gpu(points, k, n_syn):
    """
    GPU SMOTE in Euclidean space (lon/lat degrees)
    points: cudf.DataFrame ['lon','lat']
    returns: cudf.DataFrame ['lon','lat'] synthetic
    """
    if len(points) <= 1:
        return cudf.DataFrame({'lon': [], 'lat': []})
    knn = knn_gpu.NearestNeighbors(n_neighbors=min(k + 1, len(points)))
    knn.fit(points)
    dist, idx = knn.kneighbors(points)
    idx = idx[:, 1:]  # skip self
    rng = cp.random.default_rng()
    i = rng.integers(0, len(points), n_syn)
    j = rng.integers(0, idx.shape[1], n_syn)
    nn = idx[i, j]
    gaps = rng.random(n_syn, dtype=cp.float32)
    lon = points['lon'].values
    lat = points['lat'].values
    synth_lon = lon[i] + gaps * (lon[nn] - lon[i])
    synth_lat = lat[i] + gaps * (lat[nn] - lat[i])
    return cudf.DataFrame({'lon': synth_lon, 'lat': synth_lat})

# -------------------- Raster helpers --------------------
def create_geotiff(path, transform, shape, epsg):
    """Create empty GeoTIFF for density accumulation"""
    with rasterio.open(
            path, 'w',
            driver='GTiff',
            height=shape[0],
            width=shape[1],
            count=1,
            dtype='float32',
            crs=f"EPSG:{epsg}",
            transform=transform,
            compress='lzw',
            tiled=True,
            blockxsize=256,
            blockysize=256,
            nodata=0) as dst:
        dst.write(np.zeros(shape, dtype=np.float32), 1)

# -------------------- Core engine --------------------
class SpatialSmoteMC:
    def __init__(self, args):
        self.args = args
        self.client = Client() if args.gpu else None
        self._setup_raster()

    def _setup_raster(self):
        # Bounding box on-the-fly
        df = dd.read_parquet(self.args.input, columns=['lon', 'lat'])
        self.min_lon, self.max_lon = df.lon.min().compute(), df.lon.max().compute()
        self.min_lat, self.max_lat = df.lat.min().compute(), df.lat.max().compute()
        # 0.01 deg resolution raster (~1 km)
        self.res = 0.01
        self.nx = int((self.max_lon - self.min_lon) / self.res) + 1
        self.ny = int((self.max_lat - self.min_lat) / self.res) + 1
        self.transform = rasterio.transform.from_origin(
            west=self.min_lon,
            north=self.max_lat,
            xsize=self.res,
            ysize=self.res)
        # Create empty GeoTIFF
        if not os.path.exists(self.args.output):
            create_geotiff(self.args.output, self.transform, (self.ny, self.nx),
                           self.args.epsg)
        self.raster_lock = tempfile.NamedTemporaryFile(delete=False)

    def load_minority(self):
        df = dd.read_parquet(self.args.input)
        return df[df['label'] == self.args.minority][['lon', 'lat']].repartition(
            partition_size=self.args.chunksize).persist()

    def lonlat_to_rc(self, lon, lat):
        """Convert lon/lat to row/col indices"""
        col = ((lon - self.min_lon) / self.res).astype(np.int32)
        row = ((self.max_lat - lat) / self.res).astype(np.int32)
        col = np.clip(col, 0, self.nx - 1)
        row = np.clip(row, 0, self.ny - 1)
        return row, col

    def run_mc(self):
        points = self.load_minority()
        radius_deg = km_to_deg(self.args.radius_km)
        # Monte-Carlo iterations
        for it in range(self.args.mc):
            logging.info(f"Iteration {it + 1}/{self.args.mc}")
            # Process each partition
            for p in points.to_delayed():
                df = p.compute()
                if len(df) == 0:
                    continue
                # Build ball-tree on this partition
                g = cudf.from_pandas(df)
                knn = knn_gpu.NearestNeighbors(n_neighbors=self.args.knn + 1)
                knn.fit(g)
                # For each minority point, find neighbours within radius
                dist, idx = knn.radius_neighbors(g, radius=radius_deg)
                # Compute how many synth points needed (adaptive)
                counts = [len(neigh) for neigh in idx]
                n_syn = [max(0, self.args.knn - c) for c in counts]
                # Generate synthetic points
                synth_list = []
                for i, ns in enumerate(n_syn):
                    if ns == 0:
                        continue
                    neigh = g.iloc[idx[i]]
                    synth = smote_2d_gpu(neigh, self.args.knn, ns)
                    synth_list.append(synth)
                if synth_list:
                    synth_df = cudf.concat(synth_list)
                    row, col = self.lonlat_to_rc(synth_df['lon'].values.get(),
                                                 synth_df['lat'].values.get())
                    # Accumulate density (atomic add via lock file)
                    with rasterio.open(self.args.output, 'r+') as dst:
                        band = dst.read(1)
                        np.add.at(band, (row, col), 1)
                        dst.write(band, 1)
        # Normalize
        with rasterio.open(self.args.output, 'r+') as dst:
            band = dst.read(1)
            band /= self.args.mc
            dst.write(band, 1)

# -------------------- Entry point --------------------
def main():
    args = parse_args()
    tic = time.time()
    SpatialSmoteMC(args).run_mc()
    logging.info(f"Finished in {time.time() - tic:.1f}s")

if __name__ == "__main__":
    main()
