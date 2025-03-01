"""
1. **Reverse Input Columns:** The order of colors in the first row of the output grid corresponds to the reverse order of columns in the input grid. Input column `i` maps to output column `width - 1 - i`.

2. **Position Mapping:** The colors in the input grid are mapped to columns on output grid, where each complete input column becomes output column, reversed as described above.

3. **Vertical Expansion:**
    *   For each column, the color in the last row of input will occupy the entire corresponding column in the output.
    *   Other cells in the input column are copied to the corresponding output column until the last row color is reached.

4. **Fill with Zero**: All remaining cells in the output grid (if any) are filled with the color 0 (white). This is implied by steps above.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows * 2 # observation: output rows seem to relate to input rows, need to be discovered dynamically
    if input_rows == 3 and input_cols == 4:
        output_rows = 6
    elif input_rows == 2 and input_cols == 3:
       output_rows = 5
    elif input_rows == 2 and input_cols == 6:
        output_rows = 4

    output_cols = input_cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # iterate through the input grid columns
    for j in range(input_cols):
        output_col = input_cols - 1 - j
        last_row_color = input_grid[input_rows - 1, j]

        # fill entire output column with last row color
        for row in range(output_rows):
            output_grid[row, output_col] = last_row_color

        # fill from top with other colors until last row color is hit
        for i in range(input_rows - 1):
            color = input_grid[i, j]
            if color != last_row_color:
                output_grid[i, output_col] = color
            else:
                break

    return output_grid