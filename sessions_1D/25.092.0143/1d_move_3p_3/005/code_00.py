import numpy as np

"""
Identifies the single contiguous block of non-white pixels in the input row (represented as a flat list).
Shifts this block 3 positions to the right, preserving its color and length, clipping at the right boundary.
The rest of the output row remains white (0). The output is returned as a list containing the single transformed row.
"""

def find_colored_block_1d(row):
    """
    Finds the start index, end index (exclusive), and color of the first
    contiguous non-white block in a 1D list.

    Args:
        row (list[int]): The row of pixels.

    Returns:
        tuple: (start_index, end_index, color) or None if no block is found or row is empty.
    """
    row_length = len(row)
    if row_length == 0:
        return None # Handle empty row case

    start_index = -1
    color = 0

    # Iterate through the row to find the first non-white block
    for i, pixel in enumerate(row):
        # Check if the current pixel is non-white (not 0)
        if pixel != 0:
            # If we haven't started a block yet, this is the start
            if start_index == -1:
                start_index = i
                color = pixel
            # If the color changes within the block (unexpected based on examples)
            # we consider the block ended just before the color change.
            elif pixel != color:
                 return start_index, i, color
        # Check if we found a white pixel after a block had started
        elif start_index != -1:
            # This marks the end of the block (index i is the first white pixel after the block)
            return start_index, i, color

    # If a block was found and it extends to the very end of the row
    if start_index != -1:
        return start_index, row_length, color

    # If no non-white block was found after checking the whole row
    return None


def transform(input_grid):
    """
    Shifts the single colored block in the input row (list) 3 positions to the right.

    Args:
        input_grid (list[int]): A flat list representing the single input row.
                                 (Handles potential ARC format for 1D tasks).

    Returns:
        list[list[int]]: A list containing the single transformed row, matching
                         standard ARC output format.
    """
    # Assume input_grid is the flat list representing the row based on prior errors
    # and task structure.
    input_row = input_grid
    row_length = len(input_row)

    # Handle empty input case
    if row_length == 0:
        # Return an empty grid in the standard format
        return [[]]

    # Initialize the output row as a list of white pixels (0)
    output_row = [0] * row_length

    # Find the colored block's properties (start, end, color) in the input row
    block_info = find_colored_block_1d(input_row)

    # Proceed only if a colored block was actually found
    if block_info:
        start_index, end_index, color = block_info
        length = end_index - start_index # Calculate the block's length

        # Calculate the target starting index for the block in the output row
        new_start_index = start_index + 3

        # Copy the block to the new position in the output row
        # Iterate for the length of the original block
        for i in range(length):
            # Calculate the index in the output row where the current pixel of the block should go
            current_output_index = new_start_index + i

            # Check if this target index is valid (within the row boundaries)
            if 0 <= current_output_index < row_length:
                # If valid, place the block's color at this position in the output row
                output_row[current_output_index] = color
            # If the index is out of bounds (shifted off the right edge), do nothing (pixel is lost)

    # Wrap the resulting output row in a list to match the expected ARC output format [[...]]
    output_grid = [output_row]

    return output_grid