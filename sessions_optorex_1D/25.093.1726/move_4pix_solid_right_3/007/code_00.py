import numpy as np

"""
Identifies a single contiguous block of identical non-zero integers within a 12-element input sequence (NumPy array).
Shifts this block exactly 4 positions to the right, placing it into a new 12-element sequence (Python list) initialized with zeros.
The value and length of the block are preserved. Positions not occupied by the shifted block remain zero.
"""

def find_block(input_array: np.ndarray) -> tuple:
    """
    Finds the first contiguous block of identical non-zero numbers in a NumPy array.

    Args:
        input_array: A 1D NumPy array of integers.

    Returns:
        A tuple (value, start_index, end_index) representing the block's
        value (as a standard Python int), starting index (inclusive), 
        and ending index (exclusive).
        Returns (None, -1, -1) if no non-zero block is found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(input_array != 0)[0]

    # Handle edge case: no non-zero elements found in the input
    if len(non_zero_indices) == 0:
        return None, -1, -1

    # The first non-zero element marks the start of the block and its value
    start_index = non_zero_indices[0]
    # Use .item() to extract the value as a standard Python scalar type
    # This prevents the TypeError encountered previously.
    value = input_array[start_index].item() 

    # Determine the end of the contiguous block of identical values
    # Start checking from the element *after* the start_index
    end_index = start_index + 1
    # Iterate while we are within array bounds AND the current element matches the block's value
    while end_index < len(input_array) and input_array[end_index].item() == value:
        end_index += 1
        
    # The loop terminates when a different value is found or the array end is reached.
    # 'end_index' now correctly points to the first element *after* the block.

    return value, start_index, end_index


def transform(input_grid: np.ndarray) -> list:
    """
    Transforms the input NumPy array by shifting the non-zero block 4 positions right.

    Args:
        input_grid: A 1D NumPy array of 12 integers containing one non-zero block.

    Returns:
        A new list of 12 integers with the block shifted.
    """
    # Define constants based on the observed pattern and problem description
    sequence_length = 12
    shift_distance = 4

    # Initialize the output grid (as a list) with zeros
    output_list = [0] * sequence_length

    # 1. Locate the non-zero block in the input array using the helper function
    block_value, start_index, end_index = find_block(input_grid)

    # 2. Check if a valid block was found (it should always be found based on examples)
    if block_value is not None and start_index != -1:
        # 3. Calculate the new starting and ending indices for the shifted block
        new_start_index = start_index + shift_distance
        new_end_index = end_index + shift_distance

        # 4. Populate the output list with the block's value at the new position
        # Iterate through the indices where the shifted block should be placed
        for i in range(new_start_index, new_end_index):
            # 4a. Check if the target index 'i' is within the bounds of the output list
            if 0 <= i < sequence_length:
                 # 4b. Place the block's value (already a Python int) into the output list.
                 output_list[i] = block_value

    # 5. Return the modified output list
    return output_list