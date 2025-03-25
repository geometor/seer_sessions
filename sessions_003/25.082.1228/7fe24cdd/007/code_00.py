"""
1.  **Create Output Grid:** Double the dimensions of the input grid (both height and width) to create the output grid.
2.  **Copy Input (Top-Left):** Place a direct copy of the input grid into the top-left quadrant of the output grid.
3.  **Mirror Top-Right:** Copy the transposed and flipped input to the top-right quadrant. The specific transformation is equivalent to swapping rows and columns of input, *then* flipping the result left to right.
4.  **Mirror Bottom-Left:** Copy the transposed and flipped input to the bottom-left quadrant. The specific transformation is equivalent to swapping rows and columns of the input and flipping the result upside down.
5.  **Rotate 180 (Bottom-Right):** Rotate the input grid by 180 degrees and place it in the bottom-right quadrant of the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy Input (Top-Left)
    output_grid[:input_height, :input_width] = input_grid

    # Mirror Top-Right: Transpose and flip left-right
    output_grid[:input_height, input_width:] = np.fliplr(input_grid.T)

    # Mirror Bottom-Left: Transpose and flip upside-down
    output_grid[input_height:, :input_width] = np.flipud(input_grid.T)

    # Rotate 180 (Bottom-Right)
    output_grid[input_height:, input_width:] = np.rot90(input_grid, 2)

    return output_grid.tolist()