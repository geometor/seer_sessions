"""
Transforms a 1xN input grid based on the following rules:
1. Identifies a single contiguous block of a primary color (non-white 0, non-gray 5) and a single gray (5) pixel within the single row.
2. Determines the number of white (0) pixels separating the right edge of the primary color block from the gray pixel.
3. Creates an output grid of the same dimensions, initially filled with white (0).
4. Places the gray (5) pixel in the output grid at its original position (invariant).
5. Shifts the primary color block to the right by the calculated number of separating white pixels, placing it in the output grid immediately adjacent to the left of the gray pixel. All other positions remain white (0).
"""

import numpy as np

# --- Helper Functions ---

def find_pixel_index_in_row(row_1d, color):
    """Finds the index of the first occurrence of a specific color in a 1D numpy array."""
    indices = np.where(row_1d == color)[0]
    if len(indices) > 0:
        # Assuming only one gray pixel exists per task description
        return indices[0]
    return -1 # Not found

def find_color_block_in_row(row_1d):
    """
    Finds the contiguous block of non-white (0), non-gray (5) color in a 1D numpy array.
    Returns the block's color, start index, and end index.
    Returns (None, -1, -1) if no such block is found.
    """
    block_color = -1
    block_start = -1
    block_end = -1
    in_block = False
    for i, pixel in enumerate(row_1d):
        # Check if the pixel is the start of a potential block
        is_primary_color = pixel != 0 and pixel != 5
        if is_primary_color and not in_block:
            block_color = pixel
            block_start = i
            block_end = i # Initialize end index
            in_block = True
        # Check if we are continuing the block
        elif in_block and pixel == block_color:
            block_end = i # Update end index
        # Check if we just exited the block
        elif in_block and pixel != block_color:
            break # Block ended

    if block_start != -1:
        return block_color, block_start, block_end
    else:
        return None, -1, -1

def count_white_separation(row_1d, block_end_idx, gray_idx):
    """Counts white (0) pixels strictly between the block end and the gray pixel."""
    separation_count = 0
    # Ensure there's space between block and gray, and indices are valid
    if block_end_idx != -1 and gray_idx != -1 and block_end_idx < gray_idx - 1:
       # Iterate through the pixels strictly between the block end index + 1 and gray index
       for i in range(block_end_idx + 1, gray_idx):
           if row_1d[i] == 0:
               separation_count += 1
    return separation_count

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # --- Input Processing ---
    # Expecting a 1xN grid (list of one list)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        print("Warning: Unexpected input format. Expected a list containing one list.")
        return input_grid # Return input as fallback

    input_row_list = input_grid[0]
    input_row_np = np.array(input_row_list, dtype=int)
    grid_width = len(input_row_np)

    # --- Analysis ---
    # Find the gray pixel's index (anchor pixel)
    gray_idx = find_pixel_index_in_row(input_row_np, 5)
    if gray_idx == -1:
        # If gray pixel is missing, behavior is undefined by examples. Return input.
        print("Warning: Gray pixel (5) not found. Returning input grid.")
        return input_grid

    # Find the primary color block details
    block_color, block_start, block_end = find_color_block_in_row(input_row_np)
    if block_color is None:
        # If color block is missing, create output with only the gray pixel.
        print("Warning: Color block not found. Creating output with only gray pixel.")
        output_row_np = np.zeros(grid_width, dtype=int)
        output_row_np[gray_idx] = 5
        return [output_row_np.tolist()] # Return as 1xN grid

    # Calculate the number of white pixels separating the block and gray pixel
    separation_count = count_white_separation(input_row_np, block_end, gray_idx)

    # --- Output Grid Construction ---
    # Initialize output grid (row) with white (0)
    output_row_np = np.zeros(grid_width, dtype=int)

    # Place the gray pixel in the output (position is invariant)
    output_row_np[gray_idx] = 5

    # Calculate the new starting position for the block based on the shift
    new_block_start = block_start + separation_count
    block_length = block_end - block_start + 1

    # Place the color block in the output at its new calculated position
    # Check bounds before slicing to avoid errors
    if new_block_start >= 0 and (new_block_start + block_length) <= grid_width:
         output_row_np[new_block_start : new_block_start + block_length] = block_color
    else:
        # Log if the calculated position is out of bounds (shouldn't happen with valid inputs/logic)
        print(f"Warning: Calculated new block position [{new_block_start}-{new_block_start+block_length-1}] is out of bounds for grid width {grid_width}.")
        # As a fallback, might place partially if possible, but sticking to core logic for now.

    # --- Final Output ---
    # Convert the numpy row back to a list and wrap it in another list for 1xN grid format
    output_grid = [output_row_np.tolist()]
    return output_grid