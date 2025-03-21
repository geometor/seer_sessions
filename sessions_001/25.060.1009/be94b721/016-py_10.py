"""
Identify the azure (8) colored object in the input grid. Extract a subgrid 
containing the boundary of the azure object, including any adjacent white (0)
pixels. Return this subgrid.
"""

import numpy as np

def get_object_bounds(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Object not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the bounds of the azure object (color 8).
    bounds = get_object_bounds(input_grid, 8)
    if bounds is None:
        return np.zeros((0, 0), dtype=int)  # Return empty grid if object not found

    min_row, max_row, min_col, max_col = bounds

    # Extract the subgrid based on object bounds and expand it to include background
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    return output_grid