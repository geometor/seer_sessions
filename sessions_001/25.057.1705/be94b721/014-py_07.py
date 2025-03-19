"""
Extracts the largest contiguous block of azure (8) colored pixels from the input grid.
"""

import numpy as np

def find_largest_object(grid, color):
    """
    Finds the largest contiguous block of a specified color in the grid.
    Returns the bounding box coordinates (top_left_row, top_left_col, bottom_right_row, bottom_right_col)
    and the object mask.  Returns None if no object of the specified color is found.
    """
    mask = (grid == color).astype(int)
    if np.sum(mask) == 0:
        return None, None

    rows, cols = np.where(mask)
    top_left_row, top_left_col = np.min(rows), np.min(cols)
    bottom_right_row, bottom_right_col = np.max(rows), np.max(cols)

    return (top_left_row, top_left_col, bottom_right_row, bottom_right_col), mask


def transform(input_grid):
    """
    Transforms the input grid by extracting the largest azure object.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Find the largest azure (8) object
    bounding_box, _ = find_largest_object(input_grid, 8)

    # Handle cases where no azure object is found
    if bounding_box is None:
      return []

    # Extract the subgrid
    top_left_row, top_left_col, bottom_right_row, bottom_right_col = bounding_box
    output_grid = input_grid[top_left_row:bottom_right_row+1, top_left_col:bottom_right_col+1]

    return output_grid.tolist()