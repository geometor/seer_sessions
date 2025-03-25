"""
Extracts the smallest subgrid containing all non-zero pixels from the input grid.
"""

import numpy as np

def _find_bounding_box(grid):
    # Find rows and cols with non-zero elements
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    # Find min/max row and col indices
    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the non-zero subgrid from the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The extracted subgrid.
    """
    # Convert to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # Find the bounding box of the non-zero region
    min_row, max_row, min_col, max_col = _find_bounding_box(input_array)

    # Extract the subgrid using the bounding box indices.  Add 1 to max_row
    # and max_col because slicing is exclusive.
    output_grid = input_array[min_row:max_row+1, min_col:max_col+1].tolist()

    return output_grid