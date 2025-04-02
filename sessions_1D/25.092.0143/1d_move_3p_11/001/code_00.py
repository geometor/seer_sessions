import numpy as np
from typing import List, Tuple

"""
Identify the contiguous block of non-white pixels in the input grid (which is 1D). Shift this block exactly 3 positions to the right, maintaining the grid dimensions and the surrounding white pixels.
"""

def find_block(row: List[int]) -> Tuple[int, int, int]:
    """
    Finds the start index, end index (exclusive), and color of a contiguous non-white block.
    Assumes exactly one such block exists.

    Args:
        row: A list of integers representing the grid row.

    Returns:
        A tuple containing (start_index, end_index, color).
        Returns (-1, -1, -1) if no non-white block is found.
    """
    start_index = -1
    end_index = -1
    color = -1
    in_block = False

    for i, pixel in enumerate(row):
        if pixel != 0 and not in_block:
            # Found the start of the block
            start_index = i
            color = pixel
            in_block = True
        elif pixel == 0 and in_block:
            # Found the end of the block
            end_index = i
            break # Stop searching once the block ends

    # If the block extends to the end of the row
    if in_block and end_index == -1:
        end_index = len(row)

    # Handle case where no block was found
    if start_index == -1:
        return -1, -1, -1
        
    return start_index, end_index, color


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Shifts the single contiguous non-white block in a 1D input grid 3 positions to the right.

    Args:
        input_grid: A list containing a single list of integers (representing the 1D grid).

    Returns:
        A new list containing a single list of integers with the block shifted.
    """
    # Ensure input is treated as 1D
    if len(input_grid) != 1:
        # Handle unexpected input dimension, though ARC tasks usually stick to example format
        # For now, assume it's always 1 row based on examples
        pass 
        
    input_row = input_grid[0]
    height = 1
    width = len(input_row)

    # Initialize the output grid with the same dimensions, filled with white (0)
    output_row = [0] * width
    output_grid = [output_row]

    # Find the non-white block in the input row
    start_index, end_index, color = find_block(input_row)

    # If no block found, return the empty grid (or handle as error if needed)
    if start_index == -1:
        return output_grid # Return the all-white grid

    # Calculate the length of the block
    block_length = end_index - start_index

    # Calculate the new starting position for the block
    new_start_index = start_index + 3
    new_end_index = new_start_index + block_length

    # Check if the new position is within the grid bounds
    # (Based on examples, seems we don't need to handle wrapping or clipping)
    if new_end_index <= width:
        # Place the block into the output row at the new position
        for i in range(block_length):
            output_row[new_start_index + i] = color
    # else:
        # Optional: Handle cases where the shift would go out of bounds,
        # but based on ARC examples, this might not be necessary.
        # The current implementation will simply not draw the block if it fully exceeds bounds,
        # or draw a partial block if it partially exceeds bounds (due to loop range).
        # However, the loop range check (`new_end_index <= width`) prevents out-of-bounds writes.


    return output_grid