"""
The transformation rule is to identify a contiguous region of yellow (4) pixels within the input grid, determine the bounding box of this region, and then extract this bounding box as the output grid.
"""

import numpy as np

def find_object(grid, color):
    """
    Finds the bounding box of a contiguous region of a specified color.

    Args:
        grid: A 2D numpy array representing the input grid.
        color: The color value to search for.

    Returns:
        A tuple (min_row, max_row, min_col, max_col) representing the bounding box,
        or (None, None, None, None) if the color is not found.
    """
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # Return None if color not found
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by extracting the yellow (4) object.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the extracted yellow object,
        or an empty array if no yellow object is found.
    """
    # Find the bounding box of the yellow (4) region.
    min_row, max_row, min_col, max_col = find_object(input_grid, 4)

    if min_row is None:  # Handle case where yellow is not found
        return np.array([])

    # Extract the yellow region.
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid