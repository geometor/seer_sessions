import numpy as np
import math

"""
Identifies a contiguous block of identical non-zero digits within the input sequence.
Shifts this block one position to the left, adjusting the surrounding zeros 
to maintain the original sequence length. The zero immediately preceding the block 
effectively moves to the end of the sequence after the shift.
"""

def find_non_zero_block(input_grid):
    """
    Finds the start index, end index (exclusive), and value of the 
    first contiguous block of identical non-zero digits.

    Args:
        input_grid: A list or numpy array of integers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise returns (None, None, None).
    """
    start_index = -1
    end_index = -1
    value = None

    for i, val in enumerate(input_grid):
        if val != 0:
            # Found the potential start of a block
            if start_index == -1:
                start_index = i
                value = val
            # Check if the current value matches the block value
            elif val != value:
                 # This case shouldn't happen based on examples, but good to handle
                 # Assumes only ONE block exists, so we stop at the first mismatch
                 # or zero after the block started.
                 end_index = i
                 break
        elif start_index != -1:
            # Found a zero after the block started, mark the end
            end_index = i
            break

    # If the block runs to the end of the grid
    if start_index != -1 and end_index == -1:
        end_index = len(input_grid)

    # Check if a valid block was found
    if start_index != -1 and end_index != -1 and start_index < end_index:
        # Verify all elements within the identified range match the value
        block_valid = all(input_grid[j] == value for j in range(start_index, end_index))
        if block_valid:
            return start_index, end_index, value
        else:
            # This handles cases where maybe multiple different non-zero numbers appear
            # Although the examples don't show this, rescan might be needed.
            # For this specific problem constraint (one block), return None.
             return None, None, None
    else:
        return None, None, None


def transform(input_grid_str):
    """
    Transforms the input sequence string by shifting the non-zero block left.

    Args:
        input_grid_str: A string representation of the input sequence 
                          (e.g., "0 0 0 7 7 7 0 0").

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_grid = [int(x) for x in input_grid_str.split()]
    n = len(input_grid)

    # Initialize output_grid with zeros
    output_grid = [0] * n

    # Find the non-zero block in the input
    start_index, end_index, block_value = find_non_zero_block(input_grid)

    # If no block is found, or it starts at index 0 (cannot shift left)
    # return the grid filled with zeros (or handle as per specific edge case rule if needed)
    # Based on examples, a block is always present and not at index 0.
    if start_index is None or start_index == 0:
        # If no block found, maybe return input_grid? Examples suggest a block is always there.
        # Let's assume the function find_non_zero_block always finds a valid block > index 0
        # based on the provided examples. If start_index is 0, the logic might need adjustment,
        # but no example triggers this.
        # If no block is found return it as is.
        if start_index is None:
            return input_grid
        # If block starts at 0, the examples don't cover this. Returning zeros for now.
        # Re-evaluation: train_4 has block at index 1, output starts at 0. Logic holds.
        # Let's proceed assuming start_index > 0 if a block exists.
        # If start_index is None (all zeros), return all zeros is correct.


    if start_index is not None and start_index > 0 :
         # Calculate the new start and end indices for the shifted block
        new_start_index = start_index - 1
        new_end_index = end_index - 1 # block length remains the same

        # Copy the block value to the new position in the output grid
        for i in range(new_start_index, new_end_index):
             # Ensure we don't write past the buffer if block was at the very end
             if i < n:
                 output_grid[i] = block_value

    return output_grid