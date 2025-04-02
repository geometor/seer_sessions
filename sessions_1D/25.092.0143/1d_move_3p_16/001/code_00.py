import numpy as np
import sys
import os

# Add the directory containing grid_utils to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grid_utils import find_objects_by_color # Assuming a utility function exists

"""
Identifies a single contiguous block of non-white pixels in a 1D input grid (single row).
Calculates the new starting position of the block by adding 3 to its original starting index.
Creates an output grid of the same size, initially filled with white (0), and places the block at its new position.
"""

def find_non_white_block(row):
    """
    Finds the first contiguous block of non-white pixels in a 1D array.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (color, start_index, length) of the block,
               or (None, -1, -1) if no non-white block is found.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return None, -1, -1 # No non-white pixels found

    start_index = non_white_indices[0]
    color = row[start_index]
    length = 0
    # Iterate from the start index to find the end of the contiguous block
    for i in range(start_index, len(row)):
        if row[i] == color:
            length += 1
        else:
            break # End of the block

    # Verify contiguity (optional based on problem constraints, assumed true here)
    # block_indices = np.arange(start_index, start_index + length)
    # if not np.array_equal(non_white_indices, block_indices):
    #     # This indicates multiple blocks or gaps, handle as needed
    #     print("Warning: Non-contiguous non-white pixels found or multiple blocks.")
        # For this specific task, we assume only one contiguous block exists.

    return color, start_index, length


def transform(input_grid):
    """
    Shifts the single non-white block in a 1D grid 3 positions to the right.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid (expected 1 row).

    Returns:
        list[list[int]]: A 2D list representing the output grid with the shifted block.
    """
    # Convert input grid to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Ensure it's a 1-row grid as per examples
    if input_np.shape[0] != 1:
        # Handle unexpected input dimensions if necessary
        # For this task, we assume input is always 1xN
        raise ValueError("Input grid must have exactly one row.")

    input_row = input_np[0]
    height, width = input_np.shape

    # Initialize output grid with background color (white, 0)
    output_row = np.zeros_like(input_row)

    # Find the non-white block in the input row
    color, start_index, length = find_non_white_block(input_row)

    # If a block was found, shift it
    if color is not None:
        # Calculate the new starting index for the block
        new_start_index = start_index + 3

        # Extract the block segment from the input row
        block_segment = input_row[start_index : start_index + length]

        # Determine the actual range to place the block in the output, handling potential boundary issues
        # (though not seen in examples, good practice)
        place_start = new_start_index
        place_end = new_start_index + length

        # Ensure placement is within bounds (clip if necessary, though problem doesn't require it based on examples)
        if place_start < width:
             # Calculate the end index for slicing, ensuring it doesn't exceed grid width
            actual_end = min(place_end, width)
            # Calculate how much of the block fits
            block_length_to_place = actual_end - place_start
            # Place the (potentially truncated) block segment into the output row
            output_row[place_start : actual_end] = block_segment[:block_length_to_place]


    # Reshape the 1D output row back into a 2D grid (1xN)
    output_grid = output_row.reshape(1, width)

    # Convert back to list of lists for the standard ARC format
    return output_grid.tolist()