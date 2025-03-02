"""
Expands a 3x3 input grid to a 9x9 output grid. Each input cell's color dictates
the pattern within its corresponding 3x3 block in the output grid.
- Orange (7):  Fill the entire block.
- Yellow (4):  Fill top-left, top-right, bottom-left, bottom-right corners.
- Red (2): Fill top-left, top-middle and bottom-left.
- Magenta (6): Fill top-middle, top-right and middle-left.
- Background (0):  Leave the block filled with 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize 9x9 output grid with background color (0)
    output_grid = np.zeros((9, 9), dtype=int)

    # Iterate through each cell of the 3x3 input grid
    for i in range(3):
        for j in range(3):
            color = input_grid[i, j]
            # Calculate the starting row and column of the corresponding 3x3 block in the output grid
            output_block_start_row = i * 3
            output_block_start_col = j * 3

            # Apply color-specific infill rules
            if color == 7:  # Orange
                # Fill the entire 3x3 block
                output_grid[output_block_start_row:output_block_start_row+3, output_block_start_col:output_block_start_col+3] = 7
            elif color == 4:  # Yellow
                # Fill corners
                output_grid[output_block_start_row, output_block_start_col] = 4  # Top-left
                output_grid[output_block_start_row, output_block_start_col + 2] = 4  # Top-right
                output_grid[output_block_start_row + 2, output_block_start_col] = 4  # Bottom-left
                output_grid[output_block_start_row + 2, output_block_start_col + 2] = 4  # Bottom-right
            elif color == 2:  # Red
                # Fill top-left, top-middle, and bottom-left
                output_grid[output_block_start_row, output_block_start_col] = 2      # Top-left
                output_grid[output_block_start_row, output_block_start_col + 1] = 2  # Top-middle
                output_grid[output_block_start_row + 2, output_block_start_col] = 2    # Bottom-left
            elif color == 6:  # Magenta
                # Fill top-middle, top-right, and middle-left.
                output_grid[output_block_start_row, output_block_start_col + 1] = 6  # Top-middle
                output_grid[output_block_start_row, output_block_start_col + 2] = 6  # Top-right
                output_grid[output_block_start_row + 1, output_block_start_col] = 6    # Middle-left

    return output_grid