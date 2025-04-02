import numpy as np
from typing import Tuple, Optional

"""
Transforms the input grid by identifying the single contiguous horizontal block
of non-white pixels within the grid's single row and shifting this block 3
positions (columns) to the right. The output grid has the same dimensions as
the input, filled initially with the background color (white, 0), and the
shifted block is placed into it, preserving its original color and length.
Positions vacated by the block and areas not covered by the new block position
are filled with the background color.
"""

def find_object_block_in_row(row: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the start index, end index (inclusive), and color of the first
    contiguous block of non-white pixels in a 1D numpy array (a grid row).
    Assumes only one such block exists based on the task examples.

    Args:
        row: A 1D numpy array representing a single row of the grid.

    Returns:
        A tuple (start_index, end_index, color) if a block is found,
        otherwise None. Returns indices relative to the start of the row.
    """
    start_index = -1
    block_color = 0
    end_index = -1

    # Iterate through the row to find the non-white block
    for i, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1:  # Mark the start if not already started
                start_index = i
                block_color = pixel
            # Update the end index to the current position while in the block
            end_index = i
        elif start_index != -1:  # Found a background pixel after the block started
            # This marks the end of the block (at the previous index).
            # Since we assume only one block, we can return immediately.
            return start_index, end_index, block_color

    # If the loop finishes and a block was started, it means the block extends to the end of the row
    if start_index != -1:
        # The end_index would have been updated to the last index of the row in the loop
        return start_index, end_index, block_color

    # No non-white block found in the row
    return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.
                      Expected to have 1 row based on examples.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    if input_grid.ndim != 2 or input_grid.shape[0] == 0:
        # Handle invalid input shape if necessary, though examples are 1xN
        # For now, assume valid input based on examples.
        # Potentially return input or raise error for more robust handling.
        return input_grid

    height, width = input_grid.shape

    # Initialize the output grid with the background color (white=0)
    # Ensure the output has the same dimensions as the input.
    output_grid = np.zeros((height, width), dtype=int)

    # Extract the first (and only) row for processing
    # We assume the relevant action happens only on this row based on examples
    input_row = input_grid[0, :]

    # Find the non-white block in the input row
    block_info = find_object_block_in_row(input_row)

    # Proceed if a block was found
    if block_info:
        start_index, end_index, color = block_info
        block_length = end_index - start_index + 1

        # Define the shift amount
        shift_amount = 3

        # Calculate the new start column index for the shifted block
        new_start_index = start_index + shift_amount

        # Calculate the new end column index (inclusive)
        # new_end_index = new_start_index + block_length - 1

        # Ensure the new start index is within the grid bounds before placing the block
        if new_start_index < width:
            # Calculate the actual end position for slicing, considering grid boundary
            # The slice goes up to, but does not include, the end index + 1
            actual_end_slice = min(new_start_index + block_length, width)

            # Place the block (with its original color) into the first row
            # of the output grid at the new calculated position.
            output_grid[0, new_start_index : actual_end_slice] = color
            # Note: If the block is shifted partially off the grid,
            # only the part within the bounds is written.

    # Return the fully constructed output grid
    return output_grid