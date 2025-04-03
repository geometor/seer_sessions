"""
Identifies the first contiguous block of non-white pixels in the first row of a 2D input grid and shifts this block one position to the right in the output grid. The output grid has the same dimensions as the input grid, and the background color (white, 0) is maintained. Pixels shifted beyond the right boundary are omitted.
"""

import numpy as np

def find_first_non_white_block_1d(row):
    """
    Finds the first contiguous block of non-white pixels in a 1D list or array.

    Args:
        row: A 1D list or numpy array representing a single row.

    Returns:
        A tuple (color, start_index, end_index) if a block is found,
        otherwise (None, -1, -1).
        - color: The color of the non-white block.
        - start_index: The starting index (inclusive) of the block.
        - end_index: The ending index (inclusive) of the block.
    """
    start_index = -1
    end_index = -1
    block_color = None

    for i, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1: # Start of the first block
                start_index = i
                block_color = pixel
            elif pixel == block_color: # Continuation of the current block
                pass # Just continue
            else: # Found a different non-white color, block ends here
                end_index = i - 1
                break # Only find the *first* block
        elif start_index != -1: # Found a white pixel after a block started
            end_index = i - 1
            break # Block ends here

    # If the loop finished and a block started but didn't end (block goes to the end)
    if start_index != -1 and end_index == -1:
        end_index = len(row) - 1
        # Verify the last pixel is indeed part of the block (it should be if contiguous)
        if row[end_index] != block_color:
             # This case might happen if the last element was different non-white,
             # although the outer loop logic should handle it.
             # Let's assume contiguous block means it must end with the block_color.
             # If the block truly ended before the last pixel, the 'elif start_index != -1'
             # would have caught it earlier. So, if we reach here, the block extends to the end.
             pass


    # Handle the case of a single non-white pixel block correctly
    # If start_index is valid but end_index wasn't set (or set incorrectly before start)
    if start_index != -1 and end_index < start_index:
        end_index = start_index

    # If no non-white pixel was ever found
    if start_index == -1:
        return None, -1, -1

    return block_color, start_index, end_index

def transform(input_grid):
    """
    Shifts the first contiguous non-white block in the first row of the input grid
    one position to the right.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the 2D output grid with the block shifted.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize output_grid with the background color (white, 0)
    # and same dimensions as input
    output_array = np.zeros_like(input_array)

    # If there are no rows or columns, return the empty grid
    if rows == 0 or cols == 0:
        return output_array.tolist()

    # Extract the first row
    first_row = input_array[0]

    # Find the non-white block in the first row
    block_color, start_index, end_index = find_first_non_white_block_1d(first_row)

    # If a block was found, shift it in the output array's first row
    if block_color is not None:
        # Iterate through the original block's indices
        for i in range(start_index, end_index + 1):
            # Calculate the new column index (shifted right by 1)
            new_col_index = i + 1

            # Check if the new position is within the grid bounds
            if new_col_index < cols:
                # Copy the block's color to the new position in the output grid's first row
                output_array[0, new_col_index] = block_color
                
    # Copy any remaining rows (if any) from input to output unchanged
    # In this specific task based on examples, there's only one row, but for robustness:
    if rows > 1:
        output_array[1:] = input_array[1:]


    # Convert the result back to a list of lists
    return output_array.tolist()