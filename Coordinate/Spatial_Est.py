# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2024-04-30
# Description: This module is designed to estimate and correct latitudes and longitudes
#              from an image based on user-selected points.
# Usage: Use argparse to run the code on the terminal.
# ------------------------------------------------------------------------------------ #
import matplotlib.pyplot as plt
import numpy as np
import argparse

def load_figure(image_path):
    img = plt.imread(image_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    return fig, ax, img

def select_points(fig, ax, num_points, color):
    points = []

    def onclick(event):
        if num_points == float('inf') or len(points) < num_points:
            lat = event.ydata
            lon = event.xdata
            points.append((lat, lon))
            ax.plot(lon, lat, color)
            fig.canvas.draw()
        if len(points) == num_points:
            plt.close(fig)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    print(f"Click on the image to select {num_points} points.")
    plt.show()
    
    fig.canvas.mpl_disconnect(cid)
    return points

def input_lat_lon(points):
    lat_lon_points = []
    print("Enter the latitudes and longitudes for the selected points.")
    for i, (y, x) in enumerate(points):
        lat = float(input(f"Enter latitude for point {i+1} (image coordinates {x:.2f}, {y:.2f}): "))
        lon = float(input(f"Enter longitude for point {i+1} (image coordinates {x:.2f}, {y:.2f}): "))
        lat_lon_points.append((lat, lon))
    return lat_lon_points

def estimate_lat_lon(known_points, known_lat_lon, target_points):
    known_points = np.array(known_points)
    known_lat_lon = np.array(known_lat_lon)
    target_points = np.array(target_points)
    
    # Calculate the scaling factor and offset for latitude and longitude
    lat_scale = (known_lat_lon[:, 0].max() - known_lat_lon[:, 0].min()) / (known_points[:, 0].max() - known_points[:, 0].min())
    lon_scale = (known_lat_lon[:, 1].max() - known_lat_lon[:, 1].min()) / (known_points[:, 1].max() - known_points[:, 1].min())
    lat_offset = known_lat_lon[:, 0].min() - known_points[:, 0].min() * lat_scale
    lon_offset = known_lat_lon[:, 1].min() - known_points[:, 1].min() * lon_scale
    
    # Estimate latitudes and longitudes for the target points
    estimated_lat_lon = []
    for point in target_points:
        est_lat = point[0] * lat_scale + lat_offset
        est_lon = point[1] * lon_scale + lon_offset
        estimated_lat_lon.append((est_lat, est_lon))
    
    return estimated_lat_lon

def correct_lat_lon(estimated_lat_lon, lat_correction_factor, lon_correction_factor):
    corrected_lat_lon = []
    for lat, lon in estimated_lat_lon:
        corrected_lat = lat * lat_correction_factor
        corrected_lon = lon * lon_correction_factor
        corrected_lat_lon.append((corrected_lat, corrected_lon))
    return corrected_lat_lon

def main(image_path, lat_correction_factor, lon_correction_factor):
    fig, ax, img = load_figure(image_path)
    
    print("Select the four known points on the image.")
    known_points = select_points(fig, ax, num_points=4, color='ro')
    
    known_lat_lon = input_lat_lon(known_points)
    print(f"Known points (image coordinates): {known_points}")
    print(f"Known points (lat, lon): {known_lat_lon}")
    
    fig, ax, img = load_figure(image_path)
    print("Now select the target points on the image. Close the image window when done.")
    target_points = select_points(fig, ax, num_points=float('inf'), color='bo')
    
    estimated_lat_lon = estimate_lat_lon(known_points, known_lat_lon, target_points)
    print(f"Target points (image coordinates): {target_points}")
    print(f"Estimated latitudes and longitudes for target points: {estimated_lat_lon}")
    
    corrected_lat_lon = correct_lat_lon(estimated_lat_lon, lat_correction_factor, lon_correction_factor)
    print(f"Corrected latitudes and longitudes for target points: {corrected_lat_lon}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate and correct latitudes and longitudes from an image.")
    parser.add_argument('--image_path', type=str, required=True, help="Path to the image file.")
    parser.add_argument('--lat_correction_factor', type=float, required=True, help="Correction factor for latitude.")
    parser.add_argument('--lon_correction_factor', type=float, required=True, help="Correction factor for longitude.")
    
    args = parser.parse_args()
    main(args.image_path, args.lat_correction_factor, args.lon_correction_factor)
