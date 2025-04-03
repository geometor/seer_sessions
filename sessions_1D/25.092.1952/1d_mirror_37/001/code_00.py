import numpy as np
import copy

"""
Transformation Rule:
1. Identify the single maroon pixel (9) and the contiguous block of three red pixels (2 2 2) in the input grid (which is a single row).
2. Maintain the position of the maroon pixel (9) in the output grid.
3. Move the block of three red pixels (2 2 2) so that its starting position is two steps to the right of the maroon pixel's position.
4. Fill the rest of the grid with the background color (white, 0).
"""

def find_pixel_index(grid_row, color_value):
    """Finds the index of the first occurrence of a specific pixel value in a 1D array."""
    indices = np.where(grid_row == color_value)[0]
    if len(indices) > 0:
        return indices[0]
    return -1 # Not found

def find_block_start_index(grid_row, block_values):
    """Finds the starting index of a contiguous block of values in a 1D array."""
    block_len = len(block_values)
    row_len = len(grid_row)
    for i in range(row_len - block_len + 1):
        if np.array_equal(grid_row[i:i+block_len], block_values):
            return i
    return -1 # Not found

def transform(input_grid):
    """
    Moves a block of three red pixels (2 2 2) from the left side 
    of a maroon pixel (9) to its right side, maintaining a one-pixel gap.
    Assumes input_grid is a list containing a single list (1xN grid).
    """
    # Ensure input is treated as a 1D array for processing
    if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
        input_row = np.array(input_grid[0], dtype=int)
    else:
        # Handle potential variations if input format differs (e.g., already a numpy array or simple list)
        # For this specific task structure, we strongly expect the [[...]] format.
        # Adding basic handling for a simple list just in case.
        if isinstance(input_grid, list) and all(isinstance(i, int) for i in input_grid):
             input_row = np.array(input_grid, dtype=int)
        else: # Fallback or error for unexpected formats
             raise ValueError("Input grid format not recognized as 1xN")


    grid_size = len(input_row)
    background_color = 0
    maroon_color = 9
    red_block_values = np.array([2, 2, 2], dtype=int)

    # Initialize output grid with background color
    output_row = np.full(grid_size, background_color, dtype=int)

    # Find the position of the maroon pixel
    maroon_index = find_pixel_index(input_row, maroon_color)
    if maroon_index == -1:
        # Handle error: maroon pixel not found (though guaranteed by examples)
        print("Warning: Maroon pixel not found in input.")
        # Return a copy or default based on requirements if this happens
        return copy.deepcopy(input_grid) 

    # Place the maroon pixel in the output grid at the same position
    output_row[maroon_index] = maroon_color

    # Calculate the target starting position for the red block
    # It should start 2 positions to the right of the maroon pixel (maroon, gap, red_start)
    red_block_target_start_index = maroon_index + 2

    # Place the red block in the output grid
    # Ensure the block fits within the grid boundaries
    if red_block_target_start_index + len(red_block_values) <= grid_size:
        output_row[red_block_target_start_index : red_block_target_start_index + len(red_block_values)] = red_block_values
    else:
        # Handle error: red block placement goes out of bounds
        print("Warning: Red block placement out of bounds.")
        # Potentially truncate or handle as per specific task rules if this edge case occurs

    # Format output as a list of lists (1xN grid)
    output_grid = [output_row.tolist()]

    return output_grid