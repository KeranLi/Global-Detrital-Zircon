import pandas as pd
from gprm.datasets import Reconstructions
# import matplotlib.pyplot as plt
# from gprm.GPlatesReconstructionModel import PointDistributionOnSphere
# from gprm import ReconstructionModel
import pygmt
# import pygplates
import my_functions as myfunc
import numpy as np
# Import necessary libraries
import pygplates

def get_lon_lat_for_dataframe(dataframe, reconstruction_model, reconstruction_time, anchor_plate_id=0):
    """
    Reconstruct the zircon data points to their positions at a specified reconstruction time.
    
    Parameters:
    dataframe (pandas.DataFrame): The zircon data with 'Latitude' and 'Longitude' columns.
    reconstruction_model: The reconstruction model (e.g., M2021).
    reconstruction_time (float): The reconstruction time in Ma.
    anchor_plate_id (int): The anchor plate ID for reconstruction (default is 0).
    
    Returns:
    pandas.DataFrame: The zircon data with reconstructed positions.
    """
    point_features = []
    
    # Create pygplates features from the dataframe
    for index, row in dataframe.iterrows():
        try:
            point = pygplates.PointOnSphere(float(row['Latitude']), float(row['Longitude']))
            point_feature = pygplates.Feature()
            point_feature.set_geometry(point)
            point_features.append(point_feature)
        except pygplates.InvalidLatLonError:
            continue
    
    # Partition points into plates
    partitioned_point_features = pygplates.partition_into_plates(
        reconstruction_model.static_polygons,
        reconstruction_model.rotation_model,
        point_features,
        properties_to_copy=[pygplates.PartitionProperty.reconstruction_plate_id,
                            pygplates.PartitionProperty.valid_time_period]
    )
    
    partitioned_point_features_selection = []
    for partitioned_point_feature in partitioned_point_features:
        partitioned_point_features_selection.append(partitioned_point_feature)
    
    # Reconstruct the partitioned points
    reconstructed_point_features = []
    pygplates.reconstruct(
        partitioned_point_features_selection,
        reconstruction_model.rotation_model,
        reconstructed_point_features,
        reconstruction_time,
        anchor_plate_id=anchor_plate_id
    )
    
    # Extract reconstructed latitudes and longitudes
    reconstructed_lat = []
    reconstructed_lon = []
    indices = []
    for i, point in enumerate(reconstructed_point_features):
        if point.get_reconstructed_geometry() is not None:
            lat, lon = point.get_reconstructed_geometry().to_lat_lon()
            reconstructed_lat.append(lat)
            reconstructed_lon.append(lon)
            indices.append(dataframe.index[i])
    
    # Create a new dataframe for reconstructed points
    reconstructed_df = pd.DataFrame({
        'Reconstructed_Latitude': reconstructed_lat,
        'Reconstructed_Longitude': reconstructed_lon
    }, index=indices)
    
    # Merge with the original dataframe
    reconstructed_data = dataframe.join(reconstructed_df, how='inner')
    
    return reconstructed_data

# Step 1: Load and preprocess data
def load_and_preprocess_data(csv_file):
    """
    Load and preprocess zircon data from a CSV file.
    
    Parameters:
    csv_file (str): Path to the zircon data CSV file.
    
    Returns:
    pandas.DataFrame: Preprocessed zircon data.
    """
    try:
        zircon_data = pd.read_csv(csv_file, low_memory=False)
        
        # Inspect column names to identify the correct ones
        print("Column names in the dataset:", zircon_data.columns)
        
        # Update based on actual column names
        latitude_col = 'Latitude'
        longitude_col = 'Longitude'
        age_col = 'Best Age'
        
        # Drop rows with missing latitude and longitude
        zircon_data.dropna(subset=[latitude_col, longitude_col], inplace=True)
        
        # Convert relevant columns to numeric types if necessary
        zircon_data[latitude_col] = pd.to_numeric(zircon_data[latitude_col], errors='coerce')
        zircon_data[longitude_col] = pd.to_numeric(zircon_data[longitude_col], errors='coerce')
        zircon_data[age_col] = pd.to_numeric(zircon_data[age_col], errors='coerce')
        
        # Filter out rows with non-numeric latitude and longitude
        zircon_data = zircon_data.dropna(subset=[latitude_col, longitude_col])
        
        # Ensure the data types are correct
        zircon_data[latitude_col] = zircon_data[latitude_col].astype(float)
        zircon_data[longitude_col] = zircon_data[longitude_col].astype(float)
        
        return zircon_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def plot_geological_map(zircon_data, reconstruction_model, reconstruction_time, region, projection, output_file):
    """
    Plot the geological map with zircon data using reconstructed continents and plates.
    
    Parameters:
    zircon_data (pandas.DataFrame): The zircon data.
    reconstruction_model: The reconstruction model (e.g., M2021).
    reconstruction_time (float): The reconstruction time.
    region (str): The geographical region to plot.
    projection (str): The projection type for the plot.
    output_file (str): Path to save the output plot.
    """
    # Reconstruct the zircon data points
    reconstructed_zircon_data = get_lon_lat_for_dataframe(zircon_data, reconstruction_model, reconstruction_time)
    
    fig = pygmt.Figure()
    
    # Define basemap with custom frame width
    fig.basemap(region=region, projection=projection, frame=['xaf', 'yaf'])
    
    # Plot reconstructed continents and plates
    reconstructed_continents = reconstruction_model.polygon_snapshot('continents', reconstruction_time)
    reconstructed_plates = reconstruction_model.plate_snapshot(reconstruction_time, anchor_plate_id=0)
    
    reconstructed_continents.plot(fig, color='Gainsboro', pen='gray')
    reconstructed_plates.plot_other_boundaries(fig)
    reconstructed_plates.plot_mid_ocean_ridges(fig, pen='red')
    reconstructed_plates.plot_subduction_zones(fig, gap=6, size=1.2)
    
    # Filter zircon data based on reconstruction time
    filtered_zircon_data = reconstructed_zircon_data[reconstructed_zircon_data['Best Age'] <= reconstruction_time]
    
    # Plot zircon data with custom colors and styles
    fig.plot(x=filtered_zircon_data['Reconstructed_Longitude'].values, 
             y=filtered_zircon_data['Reconstructed_Latitude'].values, 
             style='c0.15c', pen='0.2p,black', color='orange', transparency=20)
    
    # Add label for reconstruction time
    fig.text(x=100, y=-70, text=f"{int(reconstruction_time)} Ma", font="9p,Helvetica-Bold,black", fill="white")
    
    # Save and show plot
    fig.savefig(output_file)
    fig.show()

def plot_geological_map_bar(zircon_data, reconstruction_model, reconstruction_time, region, projection, output_file):
    """
    Plot the geological map with zircon data using reconstructed continents and plates.
    
    Parameters:
    zircon_data (pandas.DataFrame): The zircon data.
    reconstruction_model: The reconstruction model (e.g., M2021).
    reconstruction_time (float): The reconstruction time.
    region (str): The geographical region to plot.
    projection (str): The projection type for the plot.
    output_file (str): Path to save the output plot.
    """
    # Reconstruct the zircon data points
    reconstructed_zircon_data = get_lon_lat_for_dataframe(zircon_data, reconstruction_model, reconstruction_time)
    
    fig = pygmt.Figure()
    
    # Define basemap with custom frame width
    fig.basemap(region=region, projection=projection, frame=["xaf", "yaf", "+w1p,black"])
    
    # Add coastlines
    # fig.coast(shorelines='1/1.0p,black', resolution='c', area_thresh=10000)
    
    # Plot reconstructed continents and plates
    reconstructed_continents = reconstruction_model.polygon_snapshot('continents', reconstruction_time)
    reconstructed_plates = reconstruction_model.plate_snapshot(reconstruction_time, anchor_plate_id=0)
    
    reconstructed_continents.plot(fig, color='Gainsboro', pen='gray')
    reconstructed_plates.plot_other_boundaries(fig)
    reconstructed_plates.plot_mid_ocean_ridges(fig, pen='red')
    reconstructed_plates.plot_subduction_zones(fig, gap=6, size=1.2)
    
    # Filter zircon data based on reconstruction time
    filtered_zircon_data = reconstructed_zircon_data[reconstructed_zircon_data['Best Age'] <= reconstruction_time]
    
    # Determine the 2-sigma uncertainties
    filtered_zircon_data['2_sigma'] = filtered_zircon_data.apply(
        lambda row: row['Best Age uncertainty (±2σ)'] if not pd.isnull(row['Best Age uncertainty (±2σ)']) 
        else (2 * row['Best Age uncertainty (±1σ)'] if not pd.isnull(row['Best Age uncertainty (±1σ)']) else None), 
        axis=1
    )
    
    # Remove rows with invalid 2-sigma values
    filtered_zircon_data = filtered_zircon_data.dropna(subset=['2_sigma'])
    
    # Create a color map based on the 2-sigma uncertainties
    min_uncertainty = filtered_zircon_data['2_sigma'].min()
    max_uncertainty = 1000
    pygmt.makecpt(cmap='vik', series=[min_uncertainty, max_uncertainty])
    
    # Plot zircon data with custom colors and styles
    fig.plot(
        x=filtered_zircon_data['Reconstructed_Longitude'].values, 
        y=filtered_zircon_data['Reconstructed_Latitude'].values, 
        style='c0.15c', 
        pen='0.3p,black', 
        color=filtered_zircon_data['2_sigma'].values, 
        cmap=True
    )
    
    # Add color bar with custom range and style
    fig.colorbar(frame='af+l"2 Sigma Uncertainty"', position="JBC+o0c/0.5c+w10c/0.5c+h")
    
    # Add label for reconstruction time
    fig.text(x=100, y=-70, text=f"{int(reconstruction_time)} Ma", font="9p,Helvetica-Bold,black", fill="white")
    
    # Save and show plot
    fig.savefig(output_file)
    fig.show()

def evaluate_globality_ancient(dataframe, reconstruction_model, reconstruction_time, grid_size=1):
    """
    Evaluate the globality of zircon data by calculating the proportion of activated grids in ancient times.
    
    Parameters:
    dataframe (pandas.DataFrame): The zircon data with 'Latitude' and 'Longitude' columns.
    reconstruction_model: The reconstruction model (e.g., M2021).
    reconstruction_time (float): The reconstruction time in Ma.
    grid_size (int): The size of the grid in degrees (default is 1 degree).
    
    Returns:
    float: The globality of the data.
    """
    # Reconstruct the zircon data points
    reconstructed_data = get_lon_lat_for_dataframe(dataframe, reconstruction_model, reconstruction_time)
    
    # Debug print to check reconstructed data
    # print(f"Reconstructed Data Sample:\n{reconstructed_data[['Reconstructed_Latitude', 'Reconstructed_Longitude']].head()}")
    
    # Define the latitude and longitude ranges
    lat_range = np.arange(-90, 90 + grid_size, grid_size)
    lon_range = np.arange(-180, 180 + grid_size, grid_size)
    
    # Create a 2D grid to keep track of activated cells
    grid = np.zeros((len(lat_range), len(lon_range)), dtype=int)
    
    # Iterate through the reconstructed zircon data and mark the activated grids
    for _, row in reconstructed_data.iterrows():
        lat = row['Reconstructed_Latitude']
        lon = row['Reconstructed_Longitude']
        
        # Check for valid lat/lon values before processing
        if lat is not None and lon is not None:
            # Find the corresponding grid cell
            lat_idx = int((lat + 90) // grid_size)
            lon_idx = int((lon + 180) // grid_size)
            
            # Debug print to check grid indices
            print(f"Lat: {lat}, Lon: {lon} -> Grid Cell: ({lat_idx}, {lon_idx})")
            
            # Mark the grid cell as activated
            grid[lat_idx, lon_idx] = 1
    
    # Calculate the total number of activated grids and total grids
    activated_grids = np.sum(grid)
    total_grids = grid.size
    
    # Calculate the globality
    globality = activated_grids / total_grids
    
    return globality

def evaluate_globality_ancient_light(dataframe, reconstruction_model, reconstruction_time, grid_size=1):
    """
    Evaluate the globality of zircon data by calculating the proportion of activated grids in ancient times.
    
    Parameters:
    dataframe (pandas.DataFrame): The zircon data with 'Latitude' and 'Longitude' columns.
    reconstruction_model: The reconstruction model (e.g., M2021).
    reconstruction_time (float): The reconstruction time in Ma.
    grid_size (int): The size of the grid in degrees (default is 1 degree).
    
    Returns:
    float: The globality of the data.
    """
    # Reconstruct the zircon data points
    reconstructed_data = get_lon_lat_for_dataframe(dataframe, reconstruction_model, reconstruction_time)
    
    # Convert to NumPy array for efficiency
    reconstructed_data_np = reconstructed_data[['Reconstructed_Latitude', 'Reconstructed_Longitude']].to_numpy()
    
    # Define the latitude and longitude ranges
    lat_range = np.arange(-90, 90 + grid_size, grid_size)
    lon_range = np.arange(-180, 180 + grid_size, grid_size)
    
    # Create a 2D grid to keep track of activated cells
    grid = np.zeros((len(lat_range), len(lon_range)), dtype=int)
    
    # Iterate through the reconstructed zircon data and mark the activated grids
    for lat, lon in reconstructed_data_np:
        # Check for valid lat/lon values before processing
        if not np.isnan(lat) and not np.isnan(lon):
            # Find the corresponding grid cell
            lat_idx = int((lat + 90) // grid_size)
            lon_idx = int((lon + 180) // grid_size)
            
            # Mark the grid cell as activated
            grid[lat_idx, lon_idx] = 1
    
    # Calculate the total number of activated grids and total grids
    activated_grids = np.sum(grid)
    total_grids = grid.size
    
    # Calculate the globality
    globality = activated_grids / total_grids
    
    # Explicitly delete unused variables and run garbage collection
    del reconstructed_data, reconstructed_data_np, grid
    gc.collect()
    
    return globality

from scipy.stats import gaussian_kde

def plot_kde_after_reconstruction(zircon_data, reconstruction_model, reconstruction_time, region, projection, output_file):
    """
    Plot only the KDE (Kernel Density Estimation) map for zircon data after reconstructing positions.

    Parameters:
    zircon_data (pandas.DataFrame): The zircon data.
    reconstruction_model: The reconstruction model (e.g., M2021).
    reconstruction_time (float): The reconstruction time.
    region (list): The geographical region to plot as [xmin, xmax, ymin, ymax].
    projection (str): The projection type for the plot (e.g., 'M6i').
    output_file (str): Path to save the output plot.
    """
    # Step 1: Reconstruct the zircon data points
    reconstructed_zircon_data = get_lon_lat_for_dataframe(zircon_data, reconstruction_model, reconstruction_time)
    
    # Step 2: Filter the data points based on the reconstruction time if necessary
    filtered_zircon_data = reconstructed_zircon_data[reconstructed_zircon_data['Best Age'] <= reconstruction_time]
    
    # Step 3: Extract the reconstructed coordinates (longitude and latitude)
    x = filtered_zircon_data['Reconstructed_Longitude'].values
    y = filtered_zircon_data['Reconstructed_Latitude'].values
    
    # Step 4: Create a 2D kernel density estimation (KDE) using scipy's gaussian_kde
    xy = np.vstack([x, y])
    kde = gaussian_kde(xy)
    
    # Step 5: Create grid for density estimation
    xmin, xmax, ymin, ymax = region  # Use the provided region bounds for the grid
    xi, yi = np.linspace(xmin, xmax, 500), np.linspace(ymin, ymax, 500)
    xi, yi = np.meshgrid(xi, yi)
    zi = kde(np.vstack([xi.flatten(), yi.flatten()])).reshape(xi.shape)
    
    # Step 6: Convert the KDE result to a PyGMT grid using xyz2grd
    # Convert xi, yi, and zi into a format that PyGMT understands (grid)
    df = pd.DataFrame({'x': xi.flatten(), 'y': yi.flatten(), 'z': zi.flatten()})
    
    # Calculate spacing as the difference between grid points
    lon_spacing = xi[0, 1] - xi[0, 0]
    lat_spacing = yi[1, 0] - yi[0, 0]
    
    # Ensure positive spacing values are provided to xyz2grd
    grid = pygmt.xyz2grd(df, region=region, spacing=(lon_spacing, lat_spacing))

    # Step 7: Plot the KDE density as a color map using PyGMT
    fig = pygmt.Figure()
    fig.grdimage(grid=grid, region=region, projection=projection, cmap="viridis", transparency=30)

    # Step 8: Save and show the plot
    fig.savefig(output_file)
    fig.show()



# Example usage:
# Assuming zircon_data is a pandas DataFrame with the necessary columns, and `reconstruction_model` is preloaded (e.g., M2021)
# plot_kde_after_reconstruction(zircon_data, M2021, 65, [-180, 180, -90, 90], 'M6i', 'output_kde_map.png')
# Define parameters for reconstruction
# reconstruction_time = 50  # Example reconstruction time in Ma
# projection = 'N25/10c'
# output_file = './results/geological_map_20250302_50Ma.pdf'
# Plot geological map
# M2021 = Reconstructions.fetch_Merdith2021()
# plot_geological_map(zircon_data, M2021, reconstruction_time, region, projection, output_file)