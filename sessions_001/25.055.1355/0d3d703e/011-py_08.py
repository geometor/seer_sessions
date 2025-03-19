"""
The transformation rule is a simple color substitution. Each color in the input grid is mapped to a specific color in the output grid. The mapping appears consistent across all training examples.

1.  **Color Substitution:**
    *   If the input pixel is 1, the output pixel remains 1.
    *   If the input pixel is 5, the output pixel is 9.
    *   If the input pixel is 8, the output pixel is 2.
    *   If the input pixel is 6, the output pixel is 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Define the color map
    color_map = {
        1: 1,
        5: 9,
        8: 2,
        6: 0
    }

    # Iterate over each cell in the grid
    for row_index in range(output_grid.shape[0]):
        for col_index in range(output_grid.shape[1]):
            # Get the input pixel value
            input_value = input_grid[row_index, col_index]

            # Apply color substitution based on the color_map
            if input_value in color_map:
                output_grid[row_index, col_index] = color_map[input_value]

    return output_grid