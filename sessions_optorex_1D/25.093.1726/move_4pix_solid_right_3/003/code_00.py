import numpy as np

"""
Identifies a contiguous block of identical non-zero integers in a 12-element input sequence (NumPy array).
Shifts this block exactly 4 positions to the right within a new 12-element sequence initialized with zeros.
The output is a standard Python list representing the sequence with the shifted block.
"""

def find_block_np(input_array):
    """
    Finds the first contiguous block of identical non-zero numbers in a NumPy array.

    Args:
        input_array: A 1D NumPy array of integers.

    Returns:
        A tuple (value, start_index, end_index) representing the block's
        value, starting index (inclusive), and ending index (exclusive).
        Returns (None, -1, -1) if no such block is found.
    """
    start_index = -1
    end_index = -1
    value = None
    n = len(input_array)

    # Find indices of non-zero elements
    non_zero_indices = np.where(input_array != 0)[0]

    if len(non_zero_indices) == 0:
        return None, -1, -1 # No non-zero elements found

    # The first non-zero element marks the potential start of the block
    start_index = non_zero_indices[0]
    value = input_array[start_index]

    # Iterate from the start index to find the end of the block
    for i in range(start_index, n):
        if input_array[i] != value: # Value changed or became zero
            end_index = i
            break
    else: # Loop completed without break, block goes to the end
        end_index = n
        
    # Verify if the block found is truly contiguous and identical (handles sparse non-zeros)
    # Check if all indices between start_index and end_index are in non_zero_indices
    # And if all values in that slice are equal to 'value'
    expected_indices = np.arange(start_index, end_index)
    actual_indices_in_block = non_zero_indices[(non_zero_indices >= start_index) & (non_zero_indices < end_index)]
    
    if not np.array_equal(expected_indices, actual_indices_in_block):
         # This indicates the non-zeros were not contiguous even if the first/last suggested they were
         # Or potentially multiple blocks. Re-evaluate based on the first contiguous segment.
         # Let's refine the end_index search more strictly
         value = input_array[start_index] # Reconfirm value
         for i in range(start_index + 1, n):
             if input_array[i] != value:
                 end_index = i
                 break
         else:
             end_index = n
             
         # Final check: ensure all values in the determined range are indeed 'value'
         if not np.all(input_array[start_index:end_index] == value):
              # This case implies an issue with finding the block; should not occur with problem constraints
              # For robustness, maybe return None or raise error. Sticking to original logic for now.
              pass # Assume constraints hold: one contiguous block of identical non-zeros

    # If the loop found the first non-zero but it was immediately followed by a different value or zero
    if end_index == start_index:
        end_index = start_index + 1 # A block of length 1

    return value, start_index, end_index


def transform(input_grid: np.ndarray) -> list:
    """
    Transforms the input NumPy array by shifting the non-zero block 4 positions right.

    Args:
        input_grid: A 1D NumPy array of 12 integers containing one non-zero block.

    Returns:
        A new list of 12 integers with the block shifted.
    """
    # Define constants
    sequence_length = 12
    shift_distance = 4

    # Initialize the output list with zeros
    output_list = [0] * sequence_length

    # 1. Identify the contiguous block of identical non-zero integers
    # Use the helper function adapted for NumPy arrays
    block_value, start_index, end_index = find_block_np(input_grid)

    # Check if a valid block was found
    if block_value is None or start_index == -1:
        # This case shouldn't happen based on the problem description (always one block)
        # If it did, returning the zero list is a reasonable default.
        return output_list

    # 2. Calculate the new position for the block
    new_start_index = start_index + shift_distance
    new_end_index = end_index + shift_distance

    # 3. Place the block into the output list at the new position
    # Ensure the indices stay within the bounds of the list
    # Note: range(start, end) iterates up to end-1, matching exclusive end index
    for i in range(new_start_index, new_end_index):
        # Check bounds to avoid index errors, although examples suggest it always fits
        if 0 <= i < sequence_length:
            output_list[i] = block_value

    # 4. Return the modified output sequence as a list
    return output_list