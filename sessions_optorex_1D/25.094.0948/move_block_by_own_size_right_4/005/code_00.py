"""
Transforms an input sequence by identifying a single contiguous block of identical non-zero integers, calculating its length, and shifting the block to the right by a distance equal to its length. The input might be presented as a 1D list or a 2D NumPy array with a single row; the code handles this by extracting the first row if necessary. The output is a list of integers of the same length as the input sequence, with the shifted block placed and zeros elsewhere.
"""

import numpy as np
import math # Although not used in the final logic, kept for potential future needs

def find_block(data):
    """
    Finds the first contiguous block of identical non-zero numbers in a 1D list or array.

    Args:
        data: A list or 1D numpy array of numbers.

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block (-1 if not found).
        - end_index (int): The ending index of the block (-1 if not found).
        - value (int): The value of the elements in the block (0 if not found).
        - length (int): The length of the block (0 if not found).
    """
    start_index = -1
    end_index = -1
    value = 0
    in_block = False
    n = len(data)

    for i, x in enumerate(data):
        # Look for the start of a non-zero block
        if not in_block and x != 0:
            start_index = i
            value = x
            in_block = True
        # Look for the end of the block once we are in one
        elif in_block:
            # If the current element is different from the block value,
            # or if we hit a zero, the block ends at the previous element.
            if x != value:
                end_index = i - 1
                break # Found the end

    # Handle the case where the block extends to the very end of the list
    # If we were in a block and never found its end explicitly (didn't break)
    if in_block and end_index == -1:
        end_index = n - 1

    # Calculate length if a valid block was found
    if start_index != -1:
        length = end_index - start_index + 1
        return start_index, end_index, value, length
    else:
        # No block found
        return -1, -1, 0, 0

def transform(input_grid):
    """
    Applies the block shift transformation to the input grid.

    Args:
        input_grid: Can be a list of integers, a 1D NumPy array, or a 2D NumPy
                    array with a single row representing the sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # **1. Preprocess Input:**
    # Check if input is a NumPy array and potentially 2D (shape like (1, N))
    if isinstance(input_grid, np.ndarray) and input_grid.ndim > 1:
         # Assume the relevant data is in the first row
        if input_grid.shape[0] == 1:
           input_list = input_grid[0].tolist()
        else:
             # Handle unexpected multi-row input, perhaps raise error or take first row
             # For now, taking the first row is a reasonable default based on error context
             input_list = input_grid[0].tolist()
    else:
        # Assume it's already a 1D list or array-like, convert to list
        input_list = list(input_grid)

    n = len(input_list)

    # **2. Initialize Output:**
    # Create the output list filled with zeros
    output_list = [0] * n

    # **3. Find Non-Zero Block:**
    # Use the helper function to find the block details
    start_index, end_index, value, length = find_block(input_list)

    # Proceed only if a valid block was found
    if start_index != -1:
        # **4. Calculate Shift:**
        # The shift amount is equal to the block's length
        shift_amount = length

        # **5. Calculate New Position:**
        # Determine the starting index for the block in the output list
        new_start_index = start_index + shift_amount

        # **6. Place Block in Output:**
        # Copy the block elements (the 'value') to the new position
        for i in range(length):
            # Calculate the target index in the output list
            output_idx = new_start_index + i
            # Ensure the target index is within the list bounds before writing
            if 0 <= output_idx < n:
                output_list[output_idx] = value
            # else: Optional: handle cases where shift goes out of bounds if needed

    # **7. Return Output:**
    return output_list