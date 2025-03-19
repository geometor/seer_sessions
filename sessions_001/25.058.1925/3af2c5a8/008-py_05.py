"""
1. Initialization: Create an output grid that is twice the height and twice the width of the input grid. All cells are initialized, although their initial value will be overwritten.

2. Pixel-by-Pixel Replication: Iterate through each pixel of the *input* grid. For every pixel at coordinates (x, y) in the input grid:
    *   Retrieve the color value (0-9) of the input pixel.
    *   In the *output* grid, create a 2x2 block of pixels with the *same* color. This 2x2 block will occupy the following coordinates:
        *   (2*x, 2*y)
        *   (2*x + 1, 2*y)
        *   (2*x, 2*y + 1)
        *   (2*x + 1, 2*y + 1)

3. Output: The resulting output grid is the transformed version of the input, where each original pixel is represented by a 2x2 block of the same color.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows = 2 * input_rows
    output_cols = 2 * input_cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # change output pixels 
    for i in range(input_rows):
        for j in range(input_cols):
            # Retrieve input pixel color
            color = input_grid[i, j]
            # Create 2x2 block in output grid
            output_grid[2*i, 2*j] = color
            output_grid[2*i + 1, 2*j] = color
            output_grid[2*i, 2*j + 1] = color
            output_grid[2*i + 1, 2*j + 1] = color

    return output_grid