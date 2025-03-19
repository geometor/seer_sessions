"""
Copies the bottom-right subgrid from the input grid to the output grid.
The dimensions of the output are determined by the largest square or rectangle
of non-black (non-zero) colors in the bottom right corner.
All colors present in the original input grid are preserved in the output grid.
"""

import numpy as np

def get_bottom_right_subgrid(input_grid):
    """
    Finds the bounding box of the non-black region in the bottom-right corner
    and returns the corresponding subgrid.
    """
    rows, cols = input_grid.shape
    
    # Find the bottom-right-most non-black pixel
    non_black_rows, non_black_cols = np.where(input_grid != 0)
    if len(non_black_rows) == 0:  # Handle all-black input
        return np.zeros((1,1), dtype=int) # return single black pixel

    min_row = np.min(non_black_rows)
    min_col = np.min(non_black_cols)

    # Determine the output dimensions
    output_rows = rows - min_row
    output_cols = cols - min_col


    # Extract the subgrid.
    start_row = rows - output_rows
    start_col = cols - output_cols
    output_grid = input_grid[start_row:, start_col:].copy()

    return output_grid

def transform(input_grid):
    """
    Extracts the bottom-right subgrid, preserving original input colors.
    """
    # Find and extract the non-black subgrid from the bottom-right.
    output_grid = get_bottom_right_subgrid(input_grid)

    return output_grid