import numpy as np

"""
Given a 2D input NumPy array of shape (1, N), identify the contiguous block of 
non-zero digits in the first row. Shift this block 3 positions (columns) to the 
left within the row. Create a new 2D NumPy array of the same shape, filled with 
zeros initially. Place the identified block into the new array's row at the 
shifted position, truncating the block if the shift moves it past the 
beginning (column 0).
"""

def find_non_zero_block_row(row_array):
    """
    Finds the first contiguous block of identical non-zero digits in a 1D numpy array.

    Args:
        row_array: A 1D NumPy array of integers.

    Returns:
        A tuple (value, start_index, end_index) if a block is found,
        where end_index is exclusive. Returns None if no block is found.
    """
    start_index = -1
    value = 0
    in_block = False

    for i, x in enumerate(row_array):
        if not in_block and x != 0:
            # Start of a potential block
            start_index = i
            value = x
            in_block = True
        elif in_block:
            # Check if the block ends here
            if x != value:
                # End of the block (exclusive index)
                return value, start_index, i
            # Check if the block ends at the very end of the array
            elif i == len(row_array) - 1 and x == value:
                 return value, start_index, i + 1

    # If loop finishes while in_block is true, but end condition wasn't met above
    # This shouldn't happen with the logic as written, but included for robustness
    # Or if no block was ever found
    return None 

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D NumPy array of shape (1, N) representing the input state.

    Returns:
        A 2D NumPy array of the same shape representing the transformed output state.
    """
    # Ensure input is a numpy array (might already be)
    input_grid = np.array(input_grid)

    # Validate shape (optional but good practice)
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        raise ValueError("Input grid must be a 2D NumPy array with shape (1, N)")

    # Get the shape and the single row from the input grid
    rows, cols = input_grid.shape
    input_row = input_grid[0, :] # Extract the first (and only) row

    # initialize output_grid with zeros, matching input shape
    output_grid = np.zeros_like(input_grid)
    output_row = output_grid[0, :] # Get a reference to the output row for modification

    # Find the non-zero block in the input row
    block_info = find_non_zero_block_row(input_row)

    # If a block is found, calculate its new position and place it in the output row
    if block_info:
        value, start_index, end_index = block_info
        block_length = end_index - start_index

        # Define the shift amount
        shift_amount = -3

        # Calculate the target starting column index for the block in the output row
        target_start_index = start_index + shift_amount

        # Place the block in the output row, handling boundaries
        for i in range(block_length):
            # Calculate the target column index in the output row
            target_index = target_start_index + i

            # Check if the target index is within the valid bounds of the output row
            if 0 <= target_index < cols:
                # Place the value of the block element into the output row
                output_row[target_index] = value # All elements in the block have the same 'value'

    # Return the modified output grid
    return output_grid