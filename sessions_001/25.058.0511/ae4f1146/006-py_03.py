"""
Extracts a 3x3 subgrid from the input grid if azure (8) and blue (1) pixels are present, centered around those pixels. If not, returns an empty list.
"""

import numpy as np

def find_center_of_specific_colors(grid, colors=[8, 1]):
    # Find coordinates of pixels with specified colors
    coords = np.argwhere(np.isin(grid, colors))

    if coords.size == 0:
        return None, None  # Return None if no such colors are found

    # Calculate the centroid of the found coordinates
    center_row = int(np.mean(coords[:, 0]))
    center_col = int(np.mean(coords[:, 1]))
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

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find center based on azure (8) and blue (1) pixels
    center_row, center_col = find_center_of_specific_colors(input_grid)

    # Handle cases where no azure or blue pixels are found
    if center_row is None or center_col is None:
        return []  # Return an empty grid

    # Extract 3x3 subgrid
    output_grid = extract_subgrid(input_grid, center_row, center_col)

    return output_grid.tolist()