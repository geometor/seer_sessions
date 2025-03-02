"""
Identify and extract the rectangular region of yellow (4) pixels within the input grid. Output this yellow region as a new grid.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # Return None if color not found
    # Calculate the bounding box.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the bounding box of the yellow (4) region.
    min_row, max_row, min_col, max_col = find_object(input_grid, 4)
    
    if min_row is None:  # Handle case where yellow is not found
        return np.array([])

    # Extract the yellow region.
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    return output_grid