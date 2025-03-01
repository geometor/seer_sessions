"""
1.  **Find Blue Stripe:** Locate the single-pixel-wide, full-height vertical blue stripe (color 1) in the input grid. If no blue stripe is found, return a 3-wide grid filled with 0s, with the same height as the input.
2.  **Determine Output Dimensions:** The output grid has a width of 3 and a height equal to the input grid's height.
3.  **Initialize Output:** Create an output grid filled entirely with white pixels (color 0).
4.  **Place Green Pixels (Conditional):**
    *   If input height = 1: Do not place any green pixels.
    *   If input height > 1:
        *   Place a green pixel in the last row, rightmost column (row = height - 1, column = 2).
        *   Place a green pixel at row height - 2, column = 0.
        *   If input_height >=4, place one at height -3, column=0
        *   If input_height >=5, repeat at height - 4
        *  Continue until input_height - n < 0
"""

import numpy as np

def find_vertical_stripe(grid, color):
    # Find the column index of the vertical stripe of the specified color
    height = grid.shape[0]
    for col in range(grid.shape[1]):
        if all(grid[row, col] == color for row in range(height)):
            return col
    return -1  # Return -1 if no such stripe is found

def transform(input_grid):
    # Find the column index of the blue vertical stripe (color 1)
    blue_stripe_col = find_vertical_stripe(input_grid, 1)

    # Initialize the output grid with all white pixels (color 0)
    output_height = input_grid.shape[0]
    output_width = 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # if no blue stripe is found, just return a blank grid of the appropriate size
    if (blue_stripe_col == -1):
        return output_grid

    # Place Green Pixels (Conditional)
    if output_height > 1:
        # Place a green pixel in the last row, rightmost column
        output_grid[output_height - 1, 2] = 3
        # Place a green pixel at row height - 2, column = 0.
        output_grid[output_height - 2, 0] = 3

        # Place additional green pixels
        n = 3
        while output_height - n >= 0:
            output_grid[output_height-n,0] = 3
            n += 1

    return output_grid