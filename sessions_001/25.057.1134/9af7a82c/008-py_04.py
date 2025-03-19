"""
The transformation involves iterating over the input grid's columns,
performing color sorting/replacement in each column, and using 0 as a "blank"
fill. The original colors are kept, and then 'shifted down' into the larger
output array one column at a time. The output is a 6x4 grid. Output height is
double the input height + number of rows with color 4. Output width is same.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows_with_four = np.any(input_grid == 4, axis=1)
    num_rows_with_four = np.sum(rows_with_four)
    output_height = (input_grid.shape[0] * 2) + num_rows_with_four
    output_grid = np.zeros((output_height, input_grid.shape[1]), dtype=int)

    # change output pixels
    for j in range(input_grid.shape[1]):
        # Extract unique colors from the input column, preserving order
        unique_colors = []
        for i in range(input_grid.shape[0]):
            color = input_grid[i, j]
            if color not in unique_colors:
                unique_colors.append(color)

        # Fill the output column with the unique colors, then pad with 0
        for i in range(len(unique_colors)):
            output_grid[i, j] = unique_colors[i]
        # No need for explicit padding with 0 as the array is initialized with 0s

    return output_grid