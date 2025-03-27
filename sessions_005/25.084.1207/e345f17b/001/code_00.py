"""
1. Divide the 4x8 input grid into two 4x4 subgrids: the "left grid" (columns 0-3) and the "right grid" (columns 4-7).
2. Create a new 4x4 output grid, initially filled with white (0) pixels.
3. For each cell position (row `r`, column `c`) from (0,0) to (3,3):
   a. Examine the color of the cell at `(r, c)` in the left grid.
   b. Examine the color of the cell at `(r, c)` in the right grid.
   c. If the cell in the left grid is white (0) AND the cell in the right grid is white (0), then set the color of the cell at `(r, c)` in the output grid to yellow (4).
4. Return the resulting 4x4 output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Compares the left and right 4x4 halves of the input grid.
    If a pixel is white (0) in both halves at the same relative position,
    the corresponding output pixel becomes yellow (4); otherwise, it's white (0).
    """
    # Get dimensions of the input grid
    height, width = input_grid.shape
    output_height = height
    output_width = width // 2 # Output width is half the input width

    # Extract the left and right subgrids
    left_grid = input_grid[:, :output_width]
    right_grid = input_grid[:, output_width:]

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell position in the output grid dimensions
    for r in range(output_height):
        for c in range(output_width):
            # Check the condition: pixel is white (0) in both left and right grids
            if left_grid[r, c] == 0 and right_grid[r, c] == 0:
                # Set the corresponding output pixel to yellow (4)
                output_grid[r, c] = 4
            # Otherwise, the output pixel remains white (0) as initialized

    return output_grid
