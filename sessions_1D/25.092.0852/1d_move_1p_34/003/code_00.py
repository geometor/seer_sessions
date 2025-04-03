import numpy as np

"""
Transformation Rule:
Identify the first contiguous horizontal block of non-white pixels in the input grid (which is a single-row NumPy array). 
Create an output grid of the same dimensions (NumPy array), initially filled with white pixels (0).
Place the identified block into the output grid, shifted one position to the right compared to its original starting position. Pixels shifted beyond the right boundary are discarded.
"""


def find_colored_block_np(row_array):
    """
    Finds the first contiguous block of non-white pixels in a 1D NumPy array.

    Args:
        row_array: A 1D NumPy array representing a row in the grid.

    Returns:
        A tuple (start_index, color, length) if a block is found,
        otherwise None.
        - start_index: The starting column index of the block.
        - color: The color (integer value) of the block.
        - length: The length (number of pixels) of the block.
    """
    start_index = -1
    color = 0
    length = 0
    in_block = False

    for i, pixel in enumerate(row_array):
        if not in_block and pixel != 0:  # Start of a new block
            start_index = i
            color = pixel
            length = 1
            in_block = True
        elif in_block and pixel == color:  # Continue the current block
            length += 1
        elif in_block and pixel != color:  # End of the current block (found a different color or 0)
            return start_index, color, length
        # Cases covered:
        # pixel == 0 and not in_block: continue searching
        # pixel == 0 and in_block: block just ended, handled by 'elif in_block and pixel != color:'

    # If the loop finishes while still in a block (block extends to the end)
    if in_block:
        return start_index, color, length

    return None # No non-white block found


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid (NumPy array).
    Identifies a horizontal block of color in the single row and shifts it one position to the right.

    Args:
        input_grid: A NumPy array representing the input grid (expected to be 1xN).

    Returns:
        A NumPy array representing the transformed grid.
    """
    # Validate input is a non-empty NumPy array
    if not isinstance(input_grid, np.ndarray) or input_grid.size == 0:
        # Or perhaps raise an error, depending on expected behavior for invalid input
        return np.array([[]]) # Return empty grid for invalid input

    # Get dimensions (assuming single row as per examples)
    height, width = input_grid.shape
    if height != 1:
        # Handle unexpected multi-row input if necessary, though examples don't show this.
        # For now, we'll proceed assuming height is 1.
        pass # Or raise ValueError("Input grid must have exactly one row.")

    input_row = input_grid[0] # Extract the first (and only) row

    # Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Find the colored block in the input row
    block_info = find_colored_block_np(input_row)

    # If a block is found, place it in the output grid shifted right
    if block_info:
        start_index, color, length = block_info

        # Calculate the new starting position
        new_start_index = start_index + 1

        # Determine the actual end index for slicing (exclusive)
        # It's the start index plus length
        original_end_index = start_index + length
        
        # Determine the new end index for slicing in the output
        new_end_index = new_start_index + length

        # Copy the block slice from input to the shifted position in output
        # Ensure indices are within bounds for slicing
        
        # Calculate the number of elements to actually copy (handles shifting off the edge)
        copy_length = min(length, width - new_start_index)

        if copy_length > 0:
             # Define the slice from the input row to copy
             input_slice = input_row[start_index : start_index + copy_length]
             # Define the slice in the output row to paste into
             output_slice_start = new_start_index
             output_slice_end = new_start_index + copy_length
             # Assign the values
             output_grid[0, output_slice_start:output_slice_end] = input_slice

        # Alternative (simpler numpy way if block is guaranteed contiguous color):
        # Determine the range to fill in the output grid
        # fill_start = new_start_index
        # fill_end = min(new_start_index + length, width) # Ensure not to go out of bounds
        # if fill_start < fill_end: # Check if there's anything to fill
        #    output_grid[0, fill_start:fill_end] = color


    # If no block was found, the output grid remains all zeros, which is correct.

    return output_grid