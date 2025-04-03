import numpy as np
import copy

"""
Identifies the contiguous block of non-white pixels in the input row.
Keeps the first and last pixels of this block.
Changes all pixels strictly between the first and last pixels of the block to white (0).
Pixels outside the original block remain unchanged.
"""

def find_non_white_block_indices(row):
    """
    Finds the start and end indices of the contiguous block of non-white pixels.

    Args:
        row (list or np.array): A single row of pixel values.

    Returns:
        tuple: (start_index, end_index) or (None, None) if no block found.
    """
    non_white_indices = [i for i, pixel in enumerate(row) if pixel != 0]
    if not non_white_indices:
        return None, None
    # Assuming contiguous block based on problem description
    return non_white_indices[0], non_white_indices[-1]

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A list containing a single list (the row).

    Returns:
        list of lists: The transformed grid (a list containing the modified row).
    """
    # Ensure input is treated as a 1D array/list
    # The input is technically a grid (list of lists), but here it's always 1xN
    input_row = np.array(input_grid[0])
    
    # Initialize output_grid as a copy of the input row
    output_row = input_row.copy()

    # Find the start and end indices of the non-white block
    start_index, end_index = find_non_white_block_indices(input_row)

    # If a block is found and its length is greater than 1
    if start_index is not None and end_index > start_index:
        # Iterate through the indices strictly between the start and end
        # and set the corresponding pixels in the output row to white (0)
        for i in range(start_index + 1, end_index):
            output_row[i] = 0

    # Return the modified row, wrapped in a list to match the grid format
    return [output_row.tolist()]
