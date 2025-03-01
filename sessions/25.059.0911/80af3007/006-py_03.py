"""
The transformation rule involves subsampling the input grid by a factor of 2. The output grid's dimensions are approximately half the input grid's dimensions (rounding up). The color present in the input grid, other than black (0), is identified. This non-black color from the input grid is copied to the output grid. The copying process selects pixels from the input at odd row and odd column intersections (every other row and every other column, starting from 0). These selected pixels, if they match the identified non-black color, are copied to corresponding positions in the output grid. The output grid position is calculated by dividing the input row and column indices by 2 (integer division).
"""

import numpy as np

def get_non_black_color(grid):
    """Finds the non-black color in a grid."""
    colors = np.unique(grid)
    for color in colors:
        if color != 0:
            return color
    return 0  # Return 0 if only black is present

def transform(input_grid):
    # Initialize the output grid. Dimensions are half the input, rounded up.
    input_rows, input_cols = input_grid.shape
    output_rows = (input_rows + 1) // 2
    output_cols = (input_cols + 1) // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Identify the non-black color in the input grid.
    target_color = get_non_black_color(input_grid)

    # Iterate through odd rows and columns of the input grid.
    for i in range(0, input_rows, 2):
        for j in range(0, input_cols, 2):
            # Map input indices to output indices (integer division by 2).
            output_i = i // 2
            output_j = j // 2

            # Copy the pixel value if it matches the target color.
            if input_grid[i, j] == target_color:
                output_grid[output_i, output_j] = target_color

    return output_grid