"""
Extracts the smallest subgrid containing all non-zero pixels from the input grid.
"""

import numpy as np

def get_bounding_box(grid):
    """Finds the bounding box of non-zero elements in a 2D array."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle the case of an all-zero grid
        return None  # Or return (0, 0, 0, 0) if a default is needed
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the smallest subgrid containing all non-zero pixels.
    
    Args:
        input_grid (list of lists): The input grid.
    
    Returns:
        list of lists: The extracted subgrid.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid)

    # Find the bounding box
    bounding_box = get_bounding_box(input_array)
    if bounding_box is None:
        return []

    min_row, max_row, min_col, max_col = bounding_box

    # Extract the subgrid
    output_grid = input_array[min_row:max_row+1, min_col:max_col+1].tolist()

    return output_grid