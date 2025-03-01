"""
1. Identify the Object: In the input grid, locate the contiguous block of pixels with non-zero values. This is the primary object.
2. Determine the Bounding Box: Find the minimum and maximum row and column indices of the non-zero pixels. These coordinates define the smallest rectangular bounding box enclosing the object.
3. Extract: Extract the subgrid within the input grid that is defined by the bounding box.
4. Output: The extracted subgrid is the output. If no non-zero pixels are in input, then return an empty grid.
"""

import numpy as np

def _find_bounding_box(grid):
    # Find non-zero pixels
    non_zero_indices = np.argwhere(grid != 0)

    if non_zero_indices.size == 0:  # Handle cases with no non-zero pixels
        return None  # No bounding box

    # Find min and max row/col to define the bounding box
    min_row, min_col = np.min(non_zero_indices, axis=0)
    max_row, max_col = np.max(non_zero_indices, axis=0)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    input_array = np.array(input_grid)

    # Find the bounding box
    bounding_box = _find_bounding_box(input_array)

    if bounding_box is None:
        return [] # Return an empty list, consistent with expected output type

    min_row, min_col, max_row, max_col = bounding_box

    # Extract the block
    extracted_block = input_array[min_row:max_row+1, min_col:max_col+1]
    return extracted_block.tolist() # Convert to list for the output