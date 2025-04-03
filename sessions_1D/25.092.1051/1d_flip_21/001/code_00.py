import numpy as np
import copy

# Color mapping (for potential debugging/visualization, not used in logic)
COLOR_MAP = {
    0: (238, 238, 238),  # white
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}

"""
Swap the position of a single non-white pixel with the adjacent contiguous block of different non-white pixels within a row.

1. Identify the horizontal sequence of connected non-white pixels.
2. Within this sequence, find the single pixel (pixel_A) whose color is different 
   from the pixel immediately to its right.
3. Identify the contiguous block of identically colored pixels (block_B) that 
   starts immediately to the right of pixel_A.
4. Construct the output by placing block_B where pixel_A was, and placing 
   pixel_A immediately after block_B, keeping surrounding white pixels unchanged.
"""

def find_non_white_segment(row):
    """Finds the start and end indices of the contiguous non-white segment."""
    start_idx = -1
    end_idx = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_idx == -1:
                start_idx = i
            end_idx = i
    # The segment actually ends *after* the last non-white pixel for slicing purposes
    return start_idx, end_idx + 1 if start_idx != -1 else -1


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Assumes input_grid is a 1xN grid.
    """
    # Since the grid is 1xN, extract the single row
    input_row = list(input_grid[0])
    output_row = list(input_row) # Make a copy to modify

    # Find the non-white segment
    start_idx, end_idx = find_non_white_segment(input_row)

    # If no non-white segment found, return the original grid
    if start_idx == -1:
        return input_grid # Return the original grid structure (list of lists)

    # Iterate within the segment to find the split point
    split_idx = -1
    pixel_a_color = -1
    block_b_color = -1
    for i in range(start_idx, end_idx - 1):
        current_pixel = input_row[i]
        next_pixel = input_row[i+1]
        # Check for a color change between adjacent non-white pixels
        if current_pixel != 0 and next_pixel != 0 and current_pixel != next_pixel:
            split_idx = i
            pixel_a_color = current_pixel
            block_b_color = next_pixel
            break # Found the split point

    # Check if a valid split was found (handles cases like all same non-white color)
    if split_idx != -1:
        # Determine the length of block_B
        # block_B starts at split_idx + 1 and goes up to end_idx
        block_b_length = end_idx - (split_idx + 1)

        # Construct the new sequence: block_B followed by pixel_A
        new_sequence = [block_b_color] * block_b_length + [pixel_a_color]

        # Replace the original segment in the output row with the new sequence
        output_row[start_idx:end_idx] = new_sequence

    # Return the modified row within the grid structure
    return [output_row]
