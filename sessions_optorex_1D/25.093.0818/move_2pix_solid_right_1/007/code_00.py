"""
Transforms an input sequence (list or NumPy array of 12 integers) by identifying a single contiguous block of identical non-zero integers and shifting this block 2 positions to the right within a new sequence of 12 zeros. Elements of the block that would be shifted beyond the right boundary (index 11) are discarded. If the input sequence contains no non-zero block (i.e., all zeros), the output is also a sequence of 12 zeros.
"""

import numpy as np # Import numpy as it might be the input type

def find_block(grid_list):
    """
    Finds the first contiguous block of identical non-zero numbers in a list.

    Args:
        grid_list: A list of integers.

    Returns:
        A tuple (value, start_index, end_index) representing the block's value
        and its start/end indices. Returns (None, -1, -1) if no non-zero
        block is found.
    """
    start_index = -1
    end_index = -1
    value = None
    n = len(grid_list)

    for i, val in enumerate(grid_list):
        if val != 0:
            # Found the start of a potential block
            if start_index == -1:
                start_index = i
                value = val
            # Based on examples, only one block type exists.
            # If we find a *different* non-zero value, the first block ends here.
            elif val != value:
                 end_index = i - 1
                 break
        elif start_index != -1:
            # Found a zero after the block started, mark the end
            end_index = i - 1
            break

    # Handle block extending to the very end of the grid
    if start_index != -1 and end_index == -1:
         # If we found a start but no end was marked by a 0 or different non-zero,
         # determine the true end of the *first* block by checking consistency.
         current_end = start_index
         for k in range(start_index + 1, n):
              if grid_list[k] == value:
                  current_end = k
              else:
                  break # Stop at the first element that doesn't match
         end_index = current_end

    # Check if a block was actually found
    if value is None:
        return None, -1, -1

    # Ensure end_index is valid (at least start_index) for single element blocks
    # This can happen if the block is just one element long and followed by 0 or end of list
    if end_index < start_index:
         end_index = start_index

    return value, start_index, end_index


def transform(input_grid):
    """
    Applies the block shifting transformation to the input grid.

    Args:
        input_grid: A list or NumPy array of 12 integers.

    Returns:
        A list of 12 integers representing the transformed grid.
    """
    # Convert input to list if it's a NumPy array for consistent handling
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        # Assuming it's already list-like, make a copy to avoid modifying original
        input_list = list(input_grid)

    # Assuming grid size is fixed based on examples, but using actual length is safer
    grid_size = len(input_list)
    if grid_size == 0: # Handle empty input case
        return []

    # Initialize the output grid with zeros
    output_grid = [0] * grid_size

    # Find the non-zero block in the input list using the helper function
    value, start_idx, end_idx = find_block(input_list)

    # If no block is found (value is None), return the initialized zero grid
    if value is None:
        return output_grid

    # Define the fixed shift distance
    shift_distance = 2

    # Iterate through the *original* indices of the identified block
    for i in range(start_idx, end_idx + 1):
        # Calculate the target index for the current element after shifting
        target_idx = i + shift_distance

        # Check if the calculated target index is within the valid bounds of the output grid
        if 0 <= target_idx < grid_size:
            # If within bounds, place the block's value at the target index in the output grid
            output_grid[target_idx] = value
        # Else: If target_idx is out of bounds, the element is discarded (implicitly by not placing it)

    # Return the final transformed grid as a list
    return output_grid