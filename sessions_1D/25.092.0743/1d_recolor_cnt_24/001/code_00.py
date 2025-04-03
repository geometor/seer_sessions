"""
Transforms a 1xN input grid by replacing contiguous horizontal blocks of Red (2) pixels
with blocks of the same size but different colors based on the block's length.
- Red blocks of length 1 become Maroon (9).
- Red blocks of length 2 become Blue (1).
- Red blocks of length 3 become Azure (8).
White (0) pixels remain unchanged.
"""

import numpy as np

# Define color constants for clarity
WHITE = 0
RED = 2
BLUE = 1
AZURE = 8
MAROON = 9

def find_contiguous_block_length(grid, row, start_col, target_color):
    """
    Finds the length of a contiguous horizontal block of a target color.
    """
    rows, cols = grid.shape
    length = 0
    # Check bounds and color match for the starting position
    if row < 0 or row >= rows or start_col < 0 or start_col >= cols or grid[row, start_col] != target_color:
        return 0

    # Iterate horizontally to find the length
    for c in range(start_col, cols):
        if grid[row, c] == target_color:
            length += 1
        else:
            break  # Stop when the color changes or end of grid is reached
    return length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Ensure input is a NumPy array
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape

    # Initialize output grid as a copy, as White pixels are preserved
    output_grid = np.copy(input_grid_np)

    # Define the color mapping based on length
    length_to_color_map = {
        1: MAROON,
        2: BLUE,
        3: AZURE,
    }

    # Iterate through the single row of the grid
    row = 0  # Since it's always a 1xN grid
    col = 0
    while col < cols:
        # Check if the current pixel is Red
        if input_grid_np[row, col] == RED:
            # Find the length of the contiguous Red block starting here
            block_length = find_contiguous_block_length(input_grid_np, row, col, RED)

            # Determine the output color based on the block length
            output_color = length_to_color_map.get(block_length) # Use .get for safety, though lengths 1, 2, 3 are expected

            # If a valid length and mapping exists, update the output grid
            if output_color is not None:
                for i in range(block_length):
                    if col + i < cols: # Ensure we don't write out of bounds (shouldn't happen with correct find_contiguous_block_length)
                         output_grid[row, col + i] = output_color

            # Skip past the processed block in the next iteration
            col += block_length
        else:
            # If not Red, move to the next pixel (White pixels are already copied)
            col += 1

    # Convert back to list of lists if necessary for the environment
    return output_grid.tolist()