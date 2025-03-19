"""
Extract the color values from the central 3x3 region of the input grid and use these to construct the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Get the dimensions of the input grid.
    height, width = input_array.shape
    
    # Calculate the center coordinates of the input grid.
    center_y = height // 2
    center_x = width // 2
    
    # Define the size of the central region to extract (3x3).
    region_size = 3
    
    # Calculate the starting indices for slicing the central region.
    start_y = center_y - region_size // 2
    start_x = center_x - region_size // 2
    
    # Extract the central 3x3 region from the input array.
    central_region = input_array[start_y:start_y+region_size, start_x:start_x+region_size]
    
    # Convert the extracted region to a list, which will be the output grid.
    output_grid = central_region.tolist()
    
    return output_grid