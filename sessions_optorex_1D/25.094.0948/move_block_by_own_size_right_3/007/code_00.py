"""
Transformation Rule:
Identify the single contiguous block of identical non-zero digits in the input grid's single row. 
Shift this block to the right within the row by a distance equal to its own length. 
The output grid has the same shape (1 row, N columns) as the input, with the shifted block placed in its new position and all other elements set to zero.
"""

import numpy as np

def _find_block(sequence):
    """
    Helper function to find the first contiguous block of identical non-zero digits
    in a 1D sequence (list or 1D NumPy array).

    Args:
        sequence: A list or 1D NumPy array of integers.

    Returns:
        A tuple (value, start_index, length) representing the block's digit,
        its starting index, and its length. Returns (None, -1, 0) if no 
        such block is found or if the input is empty.
    """
    if len(sequence) == 0: # Handle empty sequence case
        return None, -1, 0
        
    value = None
    start_index = -1
    length = 0
    in_block = False

    # Iterate through the sequence to find the start and extent of the block
    for i, digit in enumerate(sequence):
        # Check if the current element is non-zero
        is_non_zero = (digit != 0) 
        
        # Found the start of a potential block
        if not in_block and is_non_zero:
            value = digit
            start_index = i
            length = 1
            in_block = True
        # Continue counting if inside the block and the digit matches
        elif in_block and digit == value:
            length += 1
        # Stop searching if inside a block but the digit doesn't match or is zero
        # (Assumes only one block exists as per examples)
        elif in_block and (digit != value or not is_non_zero):
            # Found the end of the block, return its details
            return value, start_index, length

    # If we finished iterating and were still in a block (block ends at the sequence end)
    if in_block:
        return value, start_index, length
        
    # If the loop finishes without ever starting a block
    return None, -1, 0

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Identifies a contiguous block of identical non-zero digits in the single row
    of the input grid and shifts it to the right by a distance equal to the 
    block's length.

    Args:
        input_grid: A 2D NumPy array (expected shape (1, N)) representing the input.

    Returns:
        A 2D NumPy array with the same shape as input, representing the 
        transformed grid.
    """
    # Ensure input is a NumPy array
    input_grid_np = np.array(input_grid)
    
    # Verify the input grid has at least one row
    if input_grid_np.shape[0] == 0:
        return input_grid_np # Return empty grid if input is empty

    # Extract the first (and assumed only) row as the sequence to analyze
    # Using [0] indexing assumes the grid shape is (1, N)
    sequence = input_grid_np[0, :] 
    
    # Determine the dimensions of the grid (specifically width)
    grid_height, grid_width = input_grid_np.shape # Height will be 1 based on examples
    
    # Initialize the output grid with zeros, same shape and type as input
    output_grid = np.zeros_like(input_grid_np)

    # Find the non-zero block in the extracted sequence
    block_value, block_start_index, block_length = _find_block(sequence)

    # Proceed only if a valid block was found
    if block_value is not None and block_length > 0:
        # Calculate the new starting column index for the block
        # The shift distance is equal to the block's length
        new_start_index = block_start_index + block_length

        # Calculate the end index for placing the block in the output grid's row
        # Ensure the end index does not exceed the grid width
        new_end_index = min(new_start_index + block_length, grid_width)

        # Place the block into the output grid's row at the new position
        # Check if the new start index is within the grid bounds
        if new_start_index < grid_width:
             # Determine how many elements of the block actually fit
             num_elements_to_place = new_end_index - new_start_index
             if num_elements_to_place > 0:
                 # Use slicing to assign the block value to the correct range in the output row
                 output_grid[0, new_start_index:new_end_index] = block_value

    # Return the newly constructed grid with the shifted block
    return output_grid