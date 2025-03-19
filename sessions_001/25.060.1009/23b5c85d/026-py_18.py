"""
1.  **Identify Non-Zero Object:** Find the contiguous block of pixels that share the same non-zero color within the input grid. This forms a single "object".
2.  **Determine Bounding Box:** Determine the smallest rectangle (bounding box) that completely encloses the identified object.
3.  **Extract Object:** Create a new grid that has the dimensions of the bounding box.
4.  **Copy and Output:** Copy the pixel values from the input grid within the bounding box, and transfer it to the new (output) grid.
"""

import numpy as np

def find_object(grid):
    """
    Finds the bounding box of the single non-zero colored object in the grid.

    Args:
      grid: A 2D numpy array representing the grid.

    Returns:
      A tuple (top_left, bottom_right) representing the bounding box coordinates
      of the object, or None if no non-zero object is found.
    """
    non_zero_pixels = np.argwhere(grid != 0)
    if len(non_zero_pixels) == 0:
        return None  # No non-zero object found

    top_left = non_zero_pixels.min(axis=0)
    bottom_right = non_zero_pixels.max(axis=0)
    return tuple(top_left), tuple(bottom_right)

def transform(input_grid):
    """
    Extracts the single non-zero colored object from the input grid.
    """
    input_grid = np.array(input_grid)

    # Find the bounding box of the non-zero object
    bounding_box = find_object(input_grid)

    # Handle the case where no non-zero object is found.
    if bounding_box is None:
        return np.array([]).tolist() # return empty list

    top_left, bottom_right = bounding_box

    # Extract the object using array slicing
    output_grid = input_grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]

    return output_grid.tolist()