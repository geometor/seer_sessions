"""
Extracts a 3x3 subgrid from the input grid, centered around a region of interest containing azure (8) and blue (1) pixels, and filters out background (0) pixels.
"""

import numpy as np

def find_center(grid):
    # Find coordinates of non-zero pixels
    non_zero_coords = np.argwhere(grid != 0)

    if non_zero_coords.size == 0:
       return grid.shape[0] // 2, grid.shape[1] // 2

    # Calculate the centroid of non-zero pixels
    center_row = int(np.mean(non_zero_coords[:, 0]))
    center_col = int(np.mean(non_zero_coords[:, 1]))
    return center_row, center_col

def extract_subgrid(grid, center_row, center_col, size=3):
    # Calculate start and end indices for the subgrid
    start_row = max(0, center_row - size // 2)
    end_row = min(grid.shape[0], center_row + size // 2 + 1)
    start_col = max(0, center_col - size // 2)
    end_col = min(grid.shape[1], center_col + size // 2 + 1)
    
    # Extract subgrid
    subgrid = grid[start_row:end_row, start_col:end_col]
    return subgrid

def filter_background(grid):
  # Create a new grid with only the colors 1 and 8.
  rows, cols = grid.shape
  filtered_grid = np.zeros((0,0))

  center_r, center_c = find_center(grid)
  subgrid = extract_subgrid(grid, center_r, center_c)
    
  return subgrid

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find center
    center_row, center_col = find_center(input_grid)

    # Extract 3x3 subgrid
    output_grid = extract_subgrid(input_grid, center_row, center_col)
    
    #filter background
    output_grid = filter_background(output_grid)

    return output_grid.tolist()