```python
"""
Transforms an input grid into an output grid based on the presence of the digit '2' in each column. Columns with '2' are replaced with all '1's. Columns without '2' are mapped 1:1 with 0s and non-zero values in input truncated from bottom by a count of contiguous non-zero entries.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid dimensions
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])
    output_cols = 0
    output_rows = 0


    # pre-calculate output_cols
    for j in range(input_cols):
      col = [input_grid[i][j] for i in range(input_rows)]
      if 2 in col:
        output_cols +=1
      else:
        output_cols += 1

    # pre-calculate output_rows
    output_rows = input_rows

    output_grid = [[0] * output_cols for _ in range(output_rows)]

    output_col_index = 0
    for j in range(input_cols):
        col = [input_grid[i][j] for i in range(input_rows)]
        if 2 in col:
            # Fill the entire output column with '1'
            for i in range(output_rows):
                output_grid[i][output_col_index] = 1
            output_col_index += 1
        else:
            # count number of contiguous non-zero entries at the bottom of the column
            n = 0
            for i in reversed(range(input_rows)):
              if col[i] != 0:
                n += 1
              else:
                break

            # Map the input column to the output column, considering '0' and other digits, skip last n
            for i in range(output_rows - n):
                output_grid[i][output_col_index] = 1 if col[i] != 0 else 0
            output_col_index += 1

    return output_grid
```