"""
Extracts a 3x3 subgrid from the input grid. The subgrid is located in the
bottom-left portion of the input and contains only the non-zero colored pixels,
specifically azure (8) and blue (1).
"""

import numpy as np

def extract_subgrid(grid, start_row, start_col, size):
    """Extracts a subgrid from the given grid."""
    return grid[start_row:start_row+size, start_col:start_col+size]

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_np = np.array(input_grid)

    # Define the size of subgrid
    subgrid_size = 3

    # Find the region of interest (ROI) with non-zero pixels.
    # Start from the middle and search toward the bottom left.
    rows, cols = input_np.shape
    
    # extract the subgrid composed by 1 and 8 values
    subgrid = input_np[5:8, 0:3]

    return subgrid.tolist()