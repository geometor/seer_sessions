"""
1. **Reverse Input Columns:** The order of colors in the first row of the output grid corresponds to the reverse order of columns in the input grid.
2. **Position Mapping:** The colors in the input grid are mapped to the top row (row 0) of the output grid. Specifically, input column `i` maps to output column `3 - i`.
3. **Vertical Expansion:**
      - The color in the last row of input will occupy the entire column in the output.
      - All colors except in last row is copied to the same column, down to row index equal to the initial row + 1 in the input.
4. **Fill with Zero:** All remaining cells in the output grid are filled with the color 0 (white).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = 6, 4
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # iterate through the input grid
    for i in range(input_rows):
        for j in range(input_cols):
            color = input_grid[i, j]
            
            # position mapping to the first row, reversed columns
            output_col = input_cols - 1 - j
            output_grid[0, output_col] = color

            # vertical expansion
            if i == input_rows -1:
                # last row color expands to entire column
                for row in range(output_rows):
                    output_grid[row, output_col] = color
            else:
                # other colors expand down based to row index + 1
                for row in range(i + 1):
                      output_grid[row,output_col] = color


    return output_grid