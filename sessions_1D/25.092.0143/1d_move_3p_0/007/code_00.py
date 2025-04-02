"""
Transforms an input 1D grid (row) based on the following rules:
1. Finds the single contiguous block of a non-white color in the input row.
2. Calculates a new start position by shifting the block 3 positions to the right.
3. Adjusts the block's length for the output: if the block started at index 0 in the input, its output length is reduced by 1; otherwise, the length remains the same.
4. The total length of the output row is always the same as the input row length.
5. Creates the output row with the same length as the input, filled with white (0), and places the (potentially length-adjusted) block at its new calculated start position, clipped to the bounds of the output row.
"""

import numpy as np

def find_non_white_block(row):
    """
    Finds the first contiguous block of non-white pixels in a 1D array.

    Args:
        row (np.array): A 1D numpy array representing the input row.

    Returns:
        tuple: (color, start_index, length) if a block is found,
               (None, -1, 0) otherwise. Returns ints for numerical values.
    """
    # Find indices of all non-white (non-zero) pixels
    non_white_indices = np.where(row != 0)[0]
    
    # If no non-white pixels exist, return indication of no block found
    if len(non_white_indices) == 0:
        return None, -1, 0

    # The start index is the first non-white index
    start_index = non_white_indices[0]
    # The color is the value at the start index
    color = row[start_index]
    length = 0
    
    # Iterate from the start index to find the length of the contiguous block 
    # of the *same* color
    for i in range(start_index, len(row)):
        if row[i] == color:
            length += 1
        else:
            # Stop counting when a different color or the end of the row is reached
            break 

    # Ensure numerical outputs are standard Python ints
    return int(color), int(start_index), int(length)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array and ensure it's 1D
    input_array = np.array(input_grid, dtype=int)
    if input_array.ndim > 1:
         # Flatten if multi-dimensional, assuming it represents a single row conceptually
        input_row = input_array.flatten()
    else:
        input_row = input_array

    # Get the length of the input row
    input_row_length = len(input_row) # N_in

    # Step 1: Find the non-white block in the input row
    block_color, block_start_index, block_length = find_non_white_block(input_row) # C, S_in, L_in

    # Handle case where no block is found: return an all-white row of original length
    if block_color is None:
        return np.zeros(input_row_length, dtype=int).tolist()

    # Step 2: Calculate the new starting position for the block (shift right by 3)
    new_start_index = block_start_index + 3 # S_out

    # Step 3: Calculate the output block length based on the input start index
    if block_start_index == 0:
        output_block_length = block_length - 1 # L_out
    else:
        output_block_length = block_length # L_out
    # Ensure output block length is not negative
    output_block_length = max(0, output_block_length)

    # Step 4: Determine the output row length (same as input)
    output_row_length = input_row_length # N_out

    # Step 5: Create the output row, initialized with zeros (white)
    output_row = np.zeros(output_row_length, dtype=int)

    # Step 6: Place the block in the output row if its calculated length is greater than 0
    if output_block_length > 0:
        # Define the target slice indices in the output array
        place_start = new_start_index
        place_end = new_start_index + output_block_length

        # Clip the slice indices to the actual bounds of the output row (0 to N_out-1)
        actual_place_start = max(0, place_start)
        actual_place_end = min(output_row_length, place_end)

        # Only place the block if the calculated slice is valid (start < end)
        # This check handles cases where the entire block is shifted off the grid's right edge
        if actual_place_start < actual_place_end:
             # Fill the valid slice in the output row with the block color
             output_row[actual_place_start:actual_place_end] = block_color

    # Return the result as a standard Python list
    return output_row.tolist()