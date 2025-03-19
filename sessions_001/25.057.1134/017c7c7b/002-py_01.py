"""
1.  **Identify:** Locate the vertical line of blue (1) pixels in the input grid, which will always occupy the center column.
2.  **Transform:** Change the color of all the blue (1) pixels in this line to red (2).
3.  **Extend:** add three rows to the bottom of the grid.
4.  **Fill:** set the value of the cells corresponding to the location of the identified line, to the color red (2).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with increased height
    input_height, input_width = input_grid.shape
    output_height = input_height + 3
    output_grid = np.zeros((output_height, input_width), dtype=int)

    # Find the center column
    center_col = input_width // 2

    # Change blue (1) to red (2) in the original grid region and copy other colors
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 1:
                output_grid[row, col] = 2
            else:
                output_grid[row, col] = input_grid[row, col]
                
    #add three rows to bottom
    for row in range(input_height, output_height):
        output_grid[row,center_col] = 2

    return output_grid