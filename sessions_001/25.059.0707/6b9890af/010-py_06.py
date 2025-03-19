"""
The transformation extracts azure shapes from the input, creates an 8x8 grid with a red border, and positions scaled versions of the azure shapes within this new grid, preserving their relative positioning and aspect ratio, and setting the background to black.
"""

import numpy as np

def find_objects(grid, color):
    # Find objects of a specific color in the grid.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return []
    return coords

def get_bounding_box(coords):
    # Calculate the bounding box of a set of coordinates.
    min_y, min_x = np.min(coords, axis=0)
    max_y, max_x = np.max(coords, axis=0)
    return min_y, min_x, max_y, max_x
  
def get_object_size_and_center(coords):
    # Calculate object size based on bounding box.
    min_y, min_x, max_y, max_x = get_bounding_box(coords)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    center_x = (min_x + max_x) // 2
    center_y = (min_y + max_y) // 2
    return width, height, center_x, center_y

def transform(input_grid):
    # Initialize 8x8 output grid with all zeros (black).
    output_grid = np.zeros((8, 8), dtype=int)

    # Create red border.
    output_grid[0, :] = 2
    output_grid[-1, :] = 2
    output_grid[:, 0] = 2
    output_grid[:, -1] = 2
    
    # Find azure objects.
    azure_coords = find_objects(input_grid, 8)
    
    # if no azure, return
    if not azure_coords.any():
       return output_grid

    # Get azure bounding box.
    min_y, min_x, max_y, max_x = get_bounding_box(azure_coords)
    azure_width, azure_height, azure_center_x, azure_center_y = get_object_size_and_center(azure_coords)


    # Calculate scaling factors, keep aspect ratio
    scale_x = (max_x - min_x + 1) / 6
    scale_y = (max_y - min_y + 1) / 6

    scale = max(scale_x, scale_y)
    if scale == 0:
        scale = 1

    # map azure coords to output grid, scaled, centered
    for y, x in azure_coords:
        new_x = int((x - azure_center_x) / scale) + 3  # Add 4 to center horizontally
        new_y = int((y - azure_center_y) / scale) + 3  # Add 4 to center vertically

        if 0 < new_x < 7 and 0 < new_y < 7:  # within output bounds
           output_grid[new_y, new_x] = 8

    return output_grid