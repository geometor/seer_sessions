"""
The transformation identifies and extracts the smallest rectangle containing the colored cluster at the input grid's center, excluding the blue pixels (color 1).
"""

import numpy as np

def get_bounding_box(grid):
    # Find row and column indices of non-zero elements
    rows, cols = np.where(grid != 0)
    
    # Handle the case where there are no non-zero elements
    if len(rows) == 0 or len(cols) == 0:
        return 0, 0, 0, 0
        
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def get_bounding_box_exclude_color(grid, exclude_color):
    # Create a mask for non-excluded colors
    mask = (grid != 0) & (grid != exclude_color)
    rows, cols = np.where(mask)

    if len(rows) == 0 or len(cols) == 0:
      return 0,0,0,0

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col


def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)

    # Find the bounding box, excluding blue (color 1)
    min_row, max_row, min_col, max_col = get_bounding_box_exclude_color(input_array, 1)

    # Extract the cropped region
    output_grid = input_array[min_row:max_row+1, min_col:max_col+1].tolist()

    return output_grid