import numpy as np

"""
Identifies a single contiguous horizontal block of non-white pixels
in the input grid (assumed to be 1D). If the block has a length
of 3 or more pixels, it keeps the first and last pixels of this block
and changes all pixels in between to white (0). Blocks with length
1 or 2 remain unchanged. Surrounding white pixels are also unchanged.
"""

def find_block_indices_np(row_np):
    """
    Finds the start and end indices of the first contiguous non-zero block
    in a 1D NumPy array. Assumes only one such block exists per the problem description.

    Args:
        row_np: A 1D NumPy array representing a row of the grid.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no non-zero block is found.
    """
    # Find the indices of all non-white (non-zero) pixels
    non_zero_indices = np.where(row_np != 0)[0]

    # If no non-white pixels are found, return (-1, -1)
    if len(non_zero_indices) == 0:
        return -1, -1

    # Since the block is contiguous, the start index is the minimum index
    # and the end index is the maximum index.
    start_index = np.min(non_zero_indices)
    end_index = np.max(non_zero_indices)

    # Sanity check for contiguity (optional based on strict problem constraints)
    # expected_length = end_index - start_index + 1
    # if len(non_zero_indices) != expected_length:
    #     # This case should not happen based on the problem description
    #     # Handle error or return based on expected behavior if assumption is violated
    #     print("Warning: Non-contiguous block detected or multiple blocks found.")
    #     # Returning the bounds of the first detected sequence for robustness
    #     first_diff = np.diff(non_zero_indices)
    #     split_point = np.where(first_diff != 1)[0]
    #     if len(split_point) > 0:
    #         end_index = non_zero_indices[split_point[0]]


    return start_index, end_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists or NumPy array representing the 1D input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input grid to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Assuming the input is always 1D (1 row) as per examples
    if input_np.shape[0] != 1:
         # Or handle multi-row grids if the assumption changes
        raise ValueError("Input grid is expected to have exactly one row.")

    input_row = input_np[0]

    # Find the start and end column indices of the contiguous non-white block
    start_col, end_col = find_block_indices_np(input_row)

    # Create a copy of the input row to modify
    output_row = input_row.copy()

    # Check if a valid block was found
    if start_col != -1:
        # Calculate the length of the block
        block_length = end_col - start_col + 1

        # Only modify if the block has interior points (length >= 3)
        if block_length >= 3:
            # Set the interior pixels of the block to white (0)
            # Slice notation [start:end] includes start but excludes end,
            # so we need start_col + 1 and end_col
            output_row[start_col + 1 : end_col] = 0

    # Convert the modified row back to the required list of lists format
    output_grid = [output_row.tolist()]

    return output_grid