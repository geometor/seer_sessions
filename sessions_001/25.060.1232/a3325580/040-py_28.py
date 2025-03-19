"""
1. Identify Unique Colors: Examine the input grid and identify all unique non-zero pixel values (colors).
2. Determine Output Dimensions: Create an output grid that is a row vector, where the width is the number of unique colors and height is 1.
3. Populate Output Grid: Fill the output grid with the unique colors, from left to right.
"""

import numpy as np

def get_unique_colors(grid):
    # get the unique colors in the input grid, excluding 0
    return np.unique(grid[grid != 0])

def transform(input_grid):
    # get unique colors, excluding white (0)
    unique_colors = get_unique_colors(input_grid)

    # create output grid:  1 row, columns = number of unique colors
    num_colors = len(unique_colors)
    output_grid = np.zeros((1, num_colors), dtype=int)

    # fill in the output grid in row major order
    for index, val in enumerate(unique_colors):
        output_grid[0, index] = val

    return output_grid