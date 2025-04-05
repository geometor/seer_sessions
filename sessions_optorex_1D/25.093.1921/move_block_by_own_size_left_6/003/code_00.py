"""
Transforms the input grid by identifying a single contiguous block of identical 
non-zero integers in the first row and shifting this block to the left by a 
distance equal to its own length. The output is a 1D list representing the 
modified row, with the remaining positions filled with zeros.
"""

import numpy as np

def _find_non_zero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero numbers in a 1D sequence.

    Args:
        sequence: A list or 1D numpy array of integers.

    Returns:
        A tuple (value, start_index, end_index) if a block is found,
        otherwise (None, -1, -1).
        value: The non-zero integer value of the block.
        start_index: The starting index of the block (inclusive).
        end_index: The ending index of the block (inclusive).
    """
    start_index = -1
    end_index = -1
    value = None
    n = len(sequence)

    for i, num in enumerate(sequence):
        # Find the start of a potential block
        if num != 0 and start_index == -1:
            start_index = i
            value = num
        # Check if the block continues or ends
        elif start_index != -1:
            # If the current number is different from the block value, the block ends
            if num != value:
                end_index = i - 1
                break # Found the first complete block, stop searching

    # Handle case where the block started but didn't end before the loop finished
    # This means the block extends to the end of the sequence
    if start_index != -1 and end_index == -1:
         end_index = n - 1 # The block ends at the last element

    # Final check: if end_index is still -1, it means no block was found or only one element block at the very end
    # Re-validate end_index in case the loop ended precisely on the last element of the block
    if start_index != -1 and end_index == -1:
       # This check might be redundant now due to the previous block logic, but keeping for safety
       if sequence[n-1] == value:
           end_index = n - 1

    # If a block started but the value wasn't found until the end, recheck the end index properly
    # (This handles cases where the loop logic might miss the very last element in specific scenarios)
    if start_index != -1 and end_index != -1 and end_index < n - 1:
        # If the block seemed to end before the actual end, check if it should have extended further
        # This can happen if the break condition was met prematurely or logic was slightly off
        temp_end = start_index
        for k in range(start_index + 1, n):
            if sequence[k] == value:
                temp_end = k
            else:
                break # Found the first element that doesn't match
        end_index = temp_end # Correct the end_index if it extended further than initially thought


    # Ensure end_index is valid if a start_index was found
    if start_index != -1 and end_index == -1:
         # If still -1, it implies a single element block was found right at the start
         # or some edge case wasn't covered. Let's assume it ends where it started.
         end_index = start_index


    return value, start_index, end_index


def transform(input_grid):
    """
    Applies the block-shifting transformation to the input grid.

    Args:
        input_grid: A 2D numpy array, expected to have shape (1, N) or similar,
                    where the transformation logic applies to the first row.

    Returns:
        A 1D list of integers representing the transformed sequence.
    """
    # Ensure input is treated as a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Extract the first row as the sequence to process
    # Assuming the relevant data is always in the first row
    if input_grid.ndim == 0: # Handle scalar input case if necessary
        return [0] # Or appropriate handling
    elif input_grid.ndim == 1:
        input_sequence = input_grid.tolist()
    else: # Assumed 2D or higher
        input_sequence = input_grid[0, :].tolist() # Convert to list for easier processing

    n = len(input_sequence)

    # Initialize output_sequence with zeros
    output_sequence = [0] * n

    # Find the non-zero block in the input sequence
    value, start_index, end_index = _find_non_zero_block(input_sequence)

    # If no block is found (value is None or indices are -1), return the zero-filled sequence
    if value is None or start_index == -1 or end_index == -1:
        return output_sequence

    # Calculate the size of the block
    block_size = end_index - start_index + 1

    # Calculate the shift amount (equal to block size)
    shift_amount = block_size

    # Calculate the new starting index for the block in the output
    # Ensure the index stays within bounds (>= 0)
    new_start_index = max(0, start_index - shift_amount)

    # Place the block into the output sequence at the new position
    for i in range(block_size):
        output_index = new_start_index + i
        # Ensure we don't write past the end of the output sequence
        if output_index < n:
            output_sequence[output_index] = value # Use the identified block value
        else:
            # This condition should ideally not be met if logic is correct
            # for a left shift within bounds, but included for safety.
            break

    return output_sequence