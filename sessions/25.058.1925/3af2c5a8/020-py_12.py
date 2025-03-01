"""
Expands the input grid by adding a green (3) border. The height is increased by 4, and the width is increased by 2. The original content is centered within the new grid.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Calculate dimensions of the output grid
    output_height = input_height + 4
    output_width = input_width + 2


    # Initialize the output grid with green (3)
    output_grid = np.full((output_height, output_width), 3)

    # Copy the input grid into the center of the output grid
    vertical_start = 2
    horizontal_start = 1
    for i in range(input_height):
        for j in range(input_width):
            output_grid[i + vertical_start][j + horizontal_start] = input_grid[i][j]

    return output_grid