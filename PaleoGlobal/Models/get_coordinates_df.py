# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2023-12-08
# Description: This script is used to get the reconstructed coordinates for a dataframe.
# The code snippet follows https://github.com/JIANDONGCHUAN/2022_DetritalZircon_TectonicSetting_Public
# ------------------------------------------------------------------------------------ #
import pandas as pd
import pygplates

from tqdm import tqdm

def get_lon_lat_for_dataframe(dataframe, reconstruction_time, anchor_plate_id=0):
    global_rotation_model = None
    point_features = []
    for index, row in tqdm(dataframe.iterrows(), total=dataframe.shape[0], desc="Creating features"):
        try:
            point = pygplates.PointOnSphere(float(row['Latitude']), float(row['Longitude']))
            point_feature = pygplates.Feature()
            point_feature.set_geometry(point)
            point_features.append(point_feature)
        except pygplates.InvalidLatLonError:
            continue
    
    partitioned_point_features = pygplates.partition_into_plates(
        global_rotation_model.static_polygons,
        global_rotation_model.rotation_model,
        point_features,
        properties_to_copy=[pygplates.PartitionProperty.reconstruction_plate_id,
                            pygplates.PartitionProperty.valid_time_period]
    )
    
    reconstructed_point_features = []
    pygplates.reconstruct(
        partitioned_point_features,
        global_rotation_model.rotation_model,
        reconstructed_point_features,
        reconstruction_time,
        anchor_plate_id=anchor_plate_id
    )
    
    reconstructed_lat = []
    reconstructed_lon = []
    indices = []
    for i, point in enumerate(reconstructed_point_features):
        if point.get_reconstructed_geometry() is not None:
            lat, lon = point.get_reconstructed_geometry().to_lat_lon()
            reconstructed_lat.append(lat)
            reconstructed_lon.append(lon)
            indices.append(dataframe.index[i])
    
    reconstructed_df = pd.DataFrame({
        'Reconstructed_Latitude': reconstructed_lat,
        'Reconstructed_Longitude': reconstructed_lon
    }, index=indices)
    
    reconstructed_data = dataframe.join(reconstructed_df, how='inner')
    
    return reconstructed_data