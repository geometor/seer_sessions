"""
1.  **Expansion:** The output grid's height is three times the input grid's height, and its width is twice the input grid's width.
2.  **Azure Replication:** For each column in the input grid containing *any* azure (8) pixels, create *two* columns in the output grid. The first new output column is a copy of the input column (where the azure pixel now extends down the entire height of the output). The second new output column is entirely white (0) pixels.
3.  **Horizontal White Lines:** Fill every row where `row_index % 3 == 1` with white (0) pixels in the output grid and fill every row where `row_index % 3 == 2` with all white(0) pixels. This will place horizontal white rows between each original row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    output_col_index = 0
    for x in range(input_width):
        # check if azure pixel exists
        has_azure = False
        for y in range(input_height):
            if input_grid[y, x] == 8:
                has_azure = True
                break

        # copy and insert, or just increment
        if has_azure:
            # replicate azure
            for y in range(output_height):
                output_grid[y, output_col_index] = 8
            output_col_index += 1

            # insert blank column
            for y in range(output_height):
                output_grid[y, output_col_index] = 0
            output_col_index += 1
        else:
            output_col_index += 0

    # fill every other horizontal line
    for y in range(output_height):
        if y % 3 == 1:
            output_grid[y,:] = 0
        if y % 3 == 2:
            output_grid[y,:] = 0

    return output_grid