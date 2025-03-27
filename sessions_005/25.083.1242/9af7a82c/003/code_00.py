"""
1. Take the input grid.
2. Reverse the order of the columns of the input grid.
3. Create an output grid where the height is the width of the input grid plus two, and the width is the height of the input grid.
4. Populate Output:  Place each reversed column from the input grid into the rows of the output grid, starting from the top row.
5. Fill Remaining: Fill any remaining empty cells in the output grid with zeros (0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height = input_width + 2
    output_width = input_height
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Reverse the columns of the input grid
    reversed_columns = []
    for j in range(input_width - 1, -1, -1):
        reversed_columns.append(input_grid[:, j])

    # Populate the output grid with reversed columns
    for i, col in enumerate(reversed_columns):
        output_grid[i, :len(col)] = col

    return output_grid.tolist()