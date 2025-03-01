"""
1.  **Determine Output Grid Size:** The output grid is always square.  Its side length is calculated by taking the largest dimension (height or width) of the input grid, adding the smallest dimension, and then subracting 1.

2.  **Create Checkerboard Background:** Initialize the output grid with a checkerboard pattern.  Even (row + column) positions are azure (color 8), and odd positions are white (color 0).

3.  **Identify Trigger Pixels:** Locate all yellow pixels (color 4) in the *input* grid.

4. **Cross Generation:** For each yellow pixel found in the input grid, check if that position in the checkerboard is azure:
    *   If a position is azure, create a cross-shaped object centered on that position in the output grid. The cross consists of the center pixel and four pixels directly adjacent (up, down, left, right) to it, all colored yellow.
    *   If not on an azure square, do not create a cross.
"""

import numpy as np

def get_yellow_positions(grid):
    """Finds the positions of yellow pixels in a grid."""
    return np.array(np.where(grid == 4)).T.tolist()

def create_checkerboard(height, width):
    """Creates a checkerboard pattern."""
    checkerboard = np.zeros((height, width), dtype=int)
    for row in range(height):
        for col in range(width):
            if (row + col) % 2 == 0:
                checkerboard[row, col] = 8  # Azure
            else:
                checkerboard[row, col] = 0  # White
    return checkerboard

def transform(input_grid):
    # Determine Output Grid Size
    input_height, input_width = input_grid.shape
    output_size = max(input_height, input_width) + min(input_height, input_width) - 1
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Create Checkerboard Background
    output_grid[:] = create_checkerboard(output_size, output_size)

    # Identify Trigger Pixels
    input_yellow_positions = get_yellow_positions(input_grid)

    # Cross Generation
    for row, col in input_yellow_positions:
        # map input position to output
        if row < output_size and col < output_size:
            # check if checkerboard position is azure
            if (row + col) % 2 == 0:
               #create a cross
                output_grid[row, col] = 4
                if row > 0:
                    output_grid[row - 1, col] = 4  # Up
                if row < output_size - 1:
                    output_grid[row + 1, col] = 4  # Down
                if col > 0:
                    output_grid[row, col - 1] = 4  # Left
                if col < output_size - 1:
                    output_grid[row, col + 1] = 4  # Right

    return output_grid