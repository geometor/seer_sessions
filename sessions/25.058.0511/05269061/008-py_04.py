"""
Constructs a checkerboard pattern in the output grid, cycling through the distinct non-zero values observed in the input grid (1, 2, and 4), starting with 2 in the top-left cell. The output grid has the same dimensions as the input.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input grid.
    rows, cols = input_grid.shape

    # Initialize the output grid with the same dimensions.
    output_grid = np.zeros((rows, cols), dtype=int)

    # Determine the distinct non-zero values in the input (using a set to avoid duplicates).
    distinct_values = sorted(list({val for row in input_grid for val in row if val != 0}))
    # distinct values should be [1,2,4] but may vary, use index to get order right

    # Populate the output grid with the checkerboard pattern.
    for i in range(rows):
        for j in range(cols):
            # start with 2
            if (i + j) % 3 == 0:
               output_grid[i,j] = distinct_values[1] if 2 in distinct_values else distinct_values[0%len(distinct_values)] # should be '2'
            elif (i+j) % 3 == 1:
               output_grid[i,j] = distinct_values[2] if 4 in distinct_values else distinct_values[1%len(distinct_values)] # should be '4'
            else:
               output_grid[i,j] = distinct_values[0] if 1 in distinct_values else distinct_values[2%len(distinct_values)]

    return output_grid