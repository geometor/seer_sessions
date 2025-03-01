"""
The transformation extracts a subgrid of green (3) pixels from the input grid. 
The subgrid is determined by the boundaries formed by blue (1) pixels. 
The blue pixels form a rectangular frame, and the green pixels within that frame are extracted.
"""

import numpy as np

def find_blue_frame(grid):
    """Finds the outermost blue (1) pixels, forming a rectangular frame."""
    rows, cols = np.where(grid == 1)
    
    if rows.size == 0 or cols.size == 0:  # Handle cases with no blue pixels
        return None, None, None, None

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    return min_row, max_row, min_col, max_col

def extract_subgrid(grid, min_row, max_row, min_col, max_col):
    """Extracts the subgrid defined by the frame boundaries."""
    return grid[min_row + 1:max_row, min_col + 1:max_col]
    

def transform(input_grid):
    """Extracts the green subgrid defined by the blue frame."""
    # Find the boundaries of the blue frame
    min_row, max_row, min_col, max_col = find_blue_frame(input_grid)

    if min_row is None:  # Handle cases with no blue pixels
        return np.zeros((1, 1), dtype=int) # Return a 1x1 zero array by requirement

    # Extract the subgrid within the frame
    output_grid = extract_subgrid(input_grid, min_row, max_row, min_col, max_col)

    return output_grid