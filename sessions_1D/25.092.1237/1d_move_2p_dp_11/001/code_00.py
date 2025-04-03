import numpy as np
import collections

"""
Transformation Rule:
1. Identify the single blue pixel (1) in the input row. Note its position (blue_index).
2. Identify the contiguous horizontal block of non-white (0), non-blue (1) pixels located immediately to the left of a gap of white pixels preceding the blue pixel.
3. Determine the start (block_start_index) and end (block_end_index) indices and the color (block_color) of this colored block.
4. Calculate the length of the block (block_length).
5. Create the output row, initially identical to the input row.
6. Clear the original position of the colored block in the output row by setting the corresponding pixels to white (0).
7. Determine the new starting position for the block so that its rightmost pixel is adjacent to the blue pixel (new_block_start_index = blue_index - block_length).
8. Draw the colored block in its new position in the output row using its original color (block_color).
9. All other pixels, including the blue pixel and background white pixels not involved in the shift, remain unchanged.
"""

def find_blue_pixel(row):
    """Finds the index of the first blue pixel (1) in a 1D array."""
    blue_indices = np.where(row == 1)[0]
    if len(blue_indices) > 0:
        return blue_indices[0]
    return -1 # Not found

def find_colored_block_left_of_blue(row, blue_index):
    """
    Finds the contiguous block of non-white, non-blue color to the left of the blue pixel,
    separated by zero or more white pixels.
    Returns (start_index, end_index, color) or (-1, -1, -1) if not found.
    """
    if blue_index <= 0:
        return -1, -1, -1 # No space to the left

    # Scan backwards from the position left of the blue pixel
    i = blue_index - 1
    while i >= 0 and row[i] == 0: # Skip the gap (if any)
        i -= 1

    if i < 0 or row[i] == 1: # Reached the start or found blue (invalid block)
        return -1, -1, -1

    block_end_index = i
    block_color = row[block_end_index]

    if block_color == 0: # Must be a non-white block
         return -1, -1, -1

    block_start_index = block_end_index
    while block_start_index > 0 and row[block_start_index - 1] == block_color:
        block_start_index -= 1

    return block_start_index, block_end_index, block_color


def transform(input_grid):
    """
    Shifts a colored block horizontally so its right edge is adjacent 
    to the left side of a stationary blue marker pixel.
    Assumes input is a 1xN numpy array based on examples.
    """
    # Ensure input is a numpy array
    input_array = np.array(input_grid, dtype=int)

    # Handle cases where input might not be 1xN as expected by examples
    if input_array.ndim != 1 or input_array.shape[0] == 0:
         # For true 2D grids, we'd need to iterate rows or find the target row.
         # Based on examples, we assume it's always a single row (or treated as such).
         # If input is 2D like [[...]], get the first row.
         if input_array.ndim == 2 and input_array.shape[0] == 1:
             row = input_array[0]
             is_2d = True
         else:
              # Cannot process this shape based on observed pattern
              print(f"Warning: Unexpected input shape {input_array.shape}. Returning copy.")
              return input_array.copy()
    else:
        row = input_array
        is_2d = False # Input was already 1D

    # Make a copy to modify
    output_row = row.copy()
    n = len(row)

    # 1. Find the blue pixel
    blue_index = find_blue_pixel(row)
    if blue_index == -1:
        print("Warning: Blue pixel (1) not found.")
        # Return original if blue marker is missing
        return input_array.copy() 

    # 2. Find the colored block to the left
    block_start_index, block_end_index, block_color = find_colored_block_left_of_blue(row, blue_index)

    if block_start_index == -1:
        print("Warning: Could not find valid colored block left of blue pixel.")
        # Return original if no block is found
        return input_array.copy() 

    # 3. Calculate block length
    block_length = block_end_index - block_start_index + 1

    # 4. Clear the original block position in the output row
    output_row[block_start_index : block_end_index + 1] = 0

    # 5. Calculate the new starting position for the block
    # New end index should be blue_index - 1
    new_block_start_index = blue_index - block_length
    new_block_end_index = blue_index - 1 # Inclusive end index for slicing is blue_index

    # Ensure the new position is valid
    if new_block_start_index < 0:
         print(f"Warning: Calculated new block start index {new_block_start_index} is out of bounds.")
         return input_array.copy() # Cannot place block, return original

    # 6. Draw the block in the new position
    output_row[new_block_start_index : new_block_end_index + 1] = block_color

    # If original input was 2D (1xN), reshape output back
    if is_2d:
        return output_row.reshape(1, -1)
    else:
        return output_row
