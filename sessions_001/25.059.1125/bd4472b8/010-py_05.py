"""
Copies the second row of the input to the second row of the output.
Then, it takes each color in the first row of the input and creates two
rows in the output filled with that color. These pairs of rows are
appended to the output grid in the order they appear in the input's first row.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid. We know the width, and we can calculate
    # the height based on first row: 2 * len(first row) + 1 for second row
    input_grid = np.array(input_grid)
    output_height = 2 * len(input_grid[0]) + 1 +1 # + 1 because the prompt provided said len() and it's wrong
    output_grid = np.zeros((output_height, len(input_grid[0])), dtype=int)

    # Copy the second row of the input to the second row of the output
    output_grid[1, :] = input_grid[1, :]

    # Process the first row: each color generates two rows
    row_index = 2  # Start filling from the third row
    for color in input_grid[0, :]:
        output_grid[row_index, :] = color
        row_index += 1
        output_grid[row_index, :] = color
        row_index += 1


    return output_grid.tolist()