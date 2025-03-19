"""
Extract the smallest rectangular subgrid containing all non-white pixels.
Preserve the relative positions of azure (8) pixels within this subgrid.
Fill all other pixels within the subgrid with red (2).
"""

import numpy as np

def find_bounding_box(grid):
    """Find the bounding box of non-white pixels."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid case
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """Extracts a subgrid, preserves azure pixels, and fills the rest with red."""
    input_grid = np.array(input_grid)  # Ensure numpy array

    # 1. Identify Region of Interest and Extract Subgrid
    bounding_box = find_bounding_box(input_grid)
    if bounding_box is None:
      return []
      
    min_row, max_row, min_col, max_col = bounding_box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1].copy()

    # 2. Translate and Fill (combined for efficiency)
    
    output_grid[output_grid != 8] = 2
    

    return output_grid.tolist()