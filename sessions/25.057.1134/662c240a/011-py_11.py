"""
1.  Identify the Green Object: Locate all pixels with a value of 3 (green) within the input grid.
2.  Find Bounding Box: Determine the minimum and maximum row and column indices of the green pixels, forming a rectangular bounding box around the green object.
3. Extract Subgrid: Create a new grid containing only the pixels within the identified bounding box. This extracted subgrid is the output.
"""

import numpy as np

def find_green_object(input_array):
    """Finds the bounding box of the green object (pixels with value 3)."""
    green_indices = np.where(input_array == 3)
    if green_indices[0].size == 0:  # No green pixels
        return None  # Or handle the case where there's no green object
    min_row, min_col = np.min(green_indices, axis=1)
    max_row, max_col = np.max(green_indices, axis=1)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """Transforms the input grid by extracting the green object's bounding box."""
    input_array = np.array(input_grid)

    # Find the bounding box of the green object.
    bounding_box = find_green_object(input_array)

    if bounding_box is None:
        return [[]] #return empty grid

    # Extract the subgrid based on the bounding box.
    (min_row, min_col), (max_row, max_col) = bounding_box
    output_grid = input_array[min_row:max_row+1, min_col:max_col+1].tolist()

    return output_grid