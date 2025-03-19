"""
Extracts a 3x3 sub-grid centered on the last contiguous region of azure (8) pixels in the input grid.
"""

import numpy as np

def find_last_region_center(grid, color):
    # Find all pixels of the target color
    target_pixels = np.argwhere(grid == color)
    
    if target_pixels.size == 0:
        return None
    
    #assume the last occurance will be the bottom region, since that is our target
    last_occurance = target_pixels[-1]

    return (last_occurance[0], last_occurance[1])

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    
    # Find the center of the last region of azure (8) pixels
    center = find_last_region_center(input_grid, 8)
    
    if center is None:
        return None  # Or handle the case where no azure region is found

    # Define the size of the sub-grid to extract
    sub_grid_size = 3
    
    # Calculate the boundaries of the sub-grid
    row_start = max(0, center[0] - sub_grid_size // 2)
    row_end = min(input_grid.shape[0], center[0] + sub_grid_size // 2 + 1)
    col_start = max(0, center[1] - sub_grid_size // 2)
    col_end = min(input_grid.shape[1], center[1] + sub_grid_size // 2 + 1)
    
    # Extract the sub-grid
    output_grid = input_grid[row_start:row_end, col_start:col_end]
    
    return output_grid.tolist()