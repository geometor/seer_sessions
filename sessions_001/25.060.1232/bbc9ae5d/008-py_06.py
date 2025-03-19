"""
Reshapes the blue (1) region in the input grid into a square, preserving the
number of blue pixels and the y-position of the top of the shape.
"""

import numpy as np
import math

def find_blue_region(grid):
    """Finds the bounding box of the blue (1) region."""
    rows, cols = np.where(grid == 1)
    if len(rows) == 0:
        return None  # No blue region found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col, max_row, max_col)

def count_blue_pixels(grid):
    """Counts the number of blue pixels in the grid."""
    return np.sum(grid == 1)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    
    # Find the blue region
    blue_region = find_blue_region(input_grid)

    # If no blue region, return original grid
    if blue_region is None:
        return input_grid.tolist()

    # Count blue pixels
    num_blue_pixels = count_blue_pixels(input_grid)

    # Calculate side length of the output square
    side_length = int(math.ceil(math.sqrt(num_blue_pixels)))
    
    #get the y-position of original shape top
    min_row, _, _, _ = blue_region

    # Initialize output grid with zeros and the same dimensions as input
    output_grid = np.zeros_like(input_grid)

    # Fill the output shape
    row_start = min_row
    row_end = min_row + side_length
    
    col_start = blue_region[1]
    col_end = col_start + side_length
    
    if row_end > output_grid.shape[0]:
        row_end = output_grid.shape[0]
    
    if col_end > output_grid.shape[1]:
        col_end = output_grid.shape[1]    
    
    output_grid[row_start:row_end, col_start:col_end] = 1

    return output_grid.tolist()