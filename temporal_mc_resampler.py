#!/usr/bin/env python3
"""
Temporal-Monte-Carlo Resampler
==============================

Repeatedly samples random minority-class windows, adds Gaussian jitter,
and accumulates the resulting spatial density on a GeoTIFF.

Usage (single node, 8×A100):
    python temporal_mc_resampler.py \
        --input /scratch/series.zarr \
        --output density.tif \
        --minority 1 \
        --mc 5000 \
        --gpu

Usage (SLURM, 256 GPUs):
    srun -N64 --ntasks-per-node=4 \
         python temporal_mc_resampler.py [args]
"""

import argparse, logging, time, os, tempfile
import numpy as np
import cupy as cp
import zarr, rasterio
from dask.distributed import Client
import dask.array as da
import dask.dataframe as dd
from mpi4py import MPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

# -------------------- CLI --------------------
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True,
                   help="Zarr path: /path/series.zarr")
    p.add_argument("--output", required=True,
                   help="GeoTIFF/Zarr path for density raster")
    p.add_argument("--mc", type=int, default=1000,
                   help="Monte-Carlo iterations")
    p.add_argument("--minority", type=int, default=1,
                   help="Label value for minority class")
    p.add_argument("--window_len", type=int, default=30,
                   help="Length of sampled window (points)")
    p.add_argument("--sigma_time", type=float, default=0.5,
                   help="Std-dev (days) for temporal jitter")
    p.add_argument("--sigma_value", type=float, default=0.1,
                   help="Std-dev (units) for value jitter")
    p.add_argument("--gpu", action="store_true", help="Use GPU backend")
    return p.parse_args()

# -------------------- Raster helpers --------------------
def create_geotiff(path, transform, shape, epsg=4326):
    """Create an empty single-band GeoTIFF."""
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
class TemporalMCResampler:
    def __init__(self, args):
        self.args = args
        self.client = Client() if args.gpu else None
        self._setup_raster()

    def _setup_raster(self):
        # Bounding box
        ds = zarr.open(self.args.input, mode='r')
        lon = ds['lon'][:]
        lat = ds['lat'][:]
        self.min_lon, self.max_lon = float(lon.min()), float(lon.max())
        self.min_lat, self.max_lat = float(lat.min()), float(lat.max())
        self.res = 0.01  # 0.01 deg ≈ 1 km
        self.nx = int((self.max_lon - self.min_lon) / self.res) + 1
        self.ny = int((self.max_lat - self.min_lat) / self.res) + 1
        self.transform = rasterio.transform.from_origin(
            west=self.min_lon,
            north=self.max_lat,
            xsize=self.res,
            ysize=self.res)
        if RANK == 0:
            create_geotiff(self.args.output, self.transform, (self.ny, self.nx))

    def load_minority(self):
        ds = zarr.open(self.args.input, mode='r')
        df = dd.from_zarr(ds)
        return df[df['label'] == self.args.minority][
            ['timestamp', 'value', 'lon', 'lat']].persist()

    def lonlat_to_rc(self, lon, lat):
        """Convert lon/lat to row/col indices."""
        col = ((lon - self.min_lon) / self.res).astype(np.int32)
        row = ((self.max_lat - lat) / self.res).astype(np.int32)
        col = np.clip(col, 0, self.nx - 1)
        row = np.clip(row, 0, self.ny - 1)
        return row, col

    def run_mc(self):
        df = self.load_minority()
        local_trials = self.args.mc // SIZE
        if RANK == 0:
            local_trials += self.args.mc % SIZE

        # Prepare data
        data = df.compute().to_pandas() if not self.args.gpu else df.compute()

        # Monte-Carlo loop
        for trial in range(local_trials):
            logging.info(f"Rank {RANK}: trial {trial + 1}/{local_trials}")
            # Random window start
            N = len(data)
            if N <= self.args.window_len:
                continue
            start = np.random.randint(0, N - self.args.window_len + 1)
            window = data.iloc[start:start + self.args.window_len].copy()
            # Gaussian jitter
            jitter_t = np.random.normal(0, self.args.sigma_time, len(window))
            jitter_v = np.random.normal(0, self.args.sigma_value, len(window))
            window['timestamp'] += jitter_t
            window['value'] += jitter_v
            # Accumulate spatial density
            row, col = self.lonlat_to_rc(window['lon'].values,
                                         window['lat'].values)
            with rasterio.open(self.args.output, 'r+') as dst:
                band = dst.read(1)
                np.add.at(band, (row, col), 1)
                dst.write(band, 1)

        # Normalize on rank 0
        COMM.Barrier()
        if RANK == 0:
            with rasterio.open(self.args.output, 'r+') as dst:
                band = dst.read(1)
                band /= self.args.mc
                dst.write(band, 1)

# -------------------- Entry point --------------------
def main():
    args = parse_args()
    tic = time.time()
    TemporalMCResampler(args).run_mc()
    if RANK == 0:
        logging.info(f"Finished in {time.time() - tic:.1f}s")

if __name__ == "__main__":
    main()
