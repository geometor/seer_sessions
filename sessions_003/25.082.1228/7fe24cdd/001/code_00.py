"""
The input grid is expanded into a larger output grid. The output grid's dimensions are twice the height and twice the width of the input grid. The input grid is copied into the top-left quadrant of the output grid. The top-left quadrant is then mirrored horizontally to the top-right, vertically to the bottom-left, and both horizontally and vertically to the bottom-right.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Create output grid with doubled dimensions
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy input grid to top-left quadrant of output grid
    for row in range(input_height):
        for col in range(input_width):
            output_grid[row, col] = input_grid[row][col]

    # Mirror horizontally to top-right quadrant
    for row in range(input_height):
        for col in range(input_width):
            output_grid[row, output_width - 1 - col] = input_grid[row][col]

    # Mirror vertically to bottom-left quadrant
    for row in range(input_height):
        for col in range(input_width):
            output_grid[output_height - 1 - row, col] = input_grid[row][col]

    # Mirror both to bottom-right quadrant
    for row in range(input_height):
        for col in range(input_width):
            output_grid[output_height - 1 - row, output_width - 1 - col] = input_grid[row][col]

    return output_grid