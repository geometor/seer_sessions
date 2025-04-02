"""
Identifies the single contiguous block of non-white pixels in the input row.
Calculates the new starting position by adding 3 to the original starting position.
Creates a new output row of the same size, filled with the background color (white, 0).
Places the identified block (with its original color and length) into the output row starting at the calculated new position.
"""

import numpy as np

def find_non_white_block(row):
    """
    Finds the start index, length, and color of the first contiguous non-white block.
    Assumes only one such block exists.
    """
    start_index = -1
    length = 0
    color = 0
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_index == -1:
                start_index = i
                color = pixel
            length += 1
        elif start_index != -1: # End of the block found
            break
    if start_index == -1: # Handle case where no block is found (shouldn't happen based on examples)
        return None, None, None
    return start_index, length, color

def transform(input_grid):
    """
    Shifts the single horizontal non-white block 3 positions to the right.
    """
    # Convert input to numpy array for easier slicing if needed, though list ops are fine here
    # Input is expected as a list of lists, even for a single row
    input_row = input_grid[0]
    grid_width = len(input_row)
    
    # Initialize output grid with background color (white, 0)
    # Output should also be a list of lists
    output_row = [0] * grid_width

    # Find the non-white block in the input row
    start_index, length, color = find_non_white_block(input_row)

    # If no block is found (edge case), return the empty grid
    if start_index is None:
        return [output_row]

    # Calculate the new starting position
    new_start_index = start_index + 3

    # Place the block in the output row at the new position
    # Ensure the block doesn't go out of bounds (though not seen in examples)
    for i in range(length):
        current_index = new_start_index + i
        # Check bounds before writing
        if 0 <= current_index < grid_width:
            output_row[current_index] = color
            
    # Return the output grid as a list of lists
    return [output_row]
