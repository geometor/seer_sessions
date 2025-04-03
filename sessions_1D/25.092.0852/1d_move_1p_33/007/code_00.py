"""
Transforms an input grid by identifying a single contiguous block of a 
non-zero color in the first row and shifting this block exactly one position 
to the right within that row, provided there is space. The shift preserves 
the block's color and length. The transformation modifies a copy of the input 
grid and returns it. If no block is found or if the block is already at the 
rightmost edge, the original grid is returned unchanged. Assumes the input 
grid has at least one row.
"""

import numpy as np

def _find_block_in_row(row):
    """
    Finds the start index, end index, and color of the first contiguous
    non-zero block in a 1D list or numpy array.

    Args:
        row (list or np.array): A 1D sequence representing a row of the grid.

    Returns:
        tuple: (start_index, end_index, block_color) if a block is found,
               otherwise (None, None, None). Indices are integers, color is an integer.
    """
    start_index = -1
    end_index = -1
    block_color = 0
    in_block = False
    
    # Ensure row is iterable and get its length
    try:
        row_iter = list(row) # Convert potential numpy array to list for consistent iteration
        row_len = len(row_iter)
    except TypeError:
        # Handle non-iterable input gracefully
        return None, None, None

    # Iterate through the row to find the block
    for i, pixel in enumerate(row_iter):
        try:
            current_pixel = int(pixel) # Ensure comparison with integers
        except (ValueError, TypeError):
            # Treat non-integer pixels as background
            current_pixel = 0

        if current_pixel != 0 and not in_block:
            # Start of a new block
            start_index = i
            block_color = current_pixel
            in_block = True
        elif current_pixel == 0 and in_block:
            # End of the block found
            end_index = i - 1
            break # Stop searching once the first block ends

    # Handle case where the block extends to the very end of the grid
    if in_block and end_index == -1:
        end_index = row_len - 1

    # If no block was ever started, return None indicators
    if start_index == -1:
        return None, None, None

    # Return integers
    return int(start_index), int(end_index), int(block_color)


def transform(input_grid):
    """
    Transforms the input grid by shifting a colored block in the first row 
    one position to the right.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed grid.
    """
    # Handle potentially empty input grid or empty first row
    if not input_grid or not input_grid[0]:
        return [] # Return empty list for invalid input

    # Convert the input grid to a NumPy array for easier manipulation.
    # Using int type explicitly.
    try:
        input_array = np.array(input_grid, dtype=int)
    except ValueError:
         # If conversion fails (e.g., inconsistent row lengths)
         # Return the input as is or handle as an error. For ARC, consistency is expected.
         # Returning a copy to avoid modifying original potentially mutable list structure.
         return [row[:] for row in input_grid] 


    # Create a copy of the input array to modify for the output.
    # This ensures the original input_grid is not changed and handles 
    # grids with multiple rows correctly by keeping other rows unchanged initially.
    output_array = input_array.copy()

    # Focus processing on the first row
    first_row = output_array[0] 
    row_length = len(first_row)

    # Find the contiguous block of non-zero pixels in the first row
    start_index, end_index, block_color = _find_block_in_row(first_row)

    # Proceed only if a block was found
    if start_index is not None:
        # Check if the shift is possible (i.e., block is not at the right edge)
        # The new end position would be end_index + 1
        if end_index + 1 < row_length:
            # Perform the shift on the first row of the output array:
            # 1. Set the original start position to background color (0)
            first_row[start_index] = 0
            # 2. Set the position to the right of the original end to the block's color
            first_row[end_index + 1] = block_color
            # Note: Modifying 'first_row' directly modifies 'output_array[0]' 
            # because numpy slicing (output_array[0]) can return a view.
        # Else: If the block is at the right edge or cannot shift, 
        # the output_array remains the unmodified copy.

    # Convert the potentially modified NumPy array back to a list of lists format
    output_grid = output_array.tolist()

    return output_grid