```python
"""
The input grid is expanded into output grid. The height and width of output is input multiplied by factor N.
The original pattern from the input grid is replicated within the output grid.
Every column with original non-zero pixel, is followed by the insertion of a column filled entirely with color 8 (azure).
Every row with non-zero pixel is followed by insertion of the row, where value is 8 if: corresponding pixel in previous row was 0, or corresponding pixel in the next inserted column is 8.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    N = 2
    output_grid = np.zeros((input_height * N, input_width * N), dtype=int)

    # replicate input and insert new columns
    output_col = 0
    for col in range(input_width):
        output_row = 0
        for row in range(input_height):
            output_grid[output_row][output_col] = input_grid[row][col]
            output_row += 1
            # check if need to insert 8 in extra row, part 1
            if input_grid[row][col] != 0:
                output_grid[output_row][output_col] = 8
        output_col += 1

        # insert column of 8s
        if np.any(input_grid[:, col] != 0):
          output_row = 0
          for row in range(input_height):
            output_grid[output_row][output_col] = 8
            output_row += 1
            # check if need to insert 8 in extra row, part 2
            output_grid[output_row][output_col] = 8
          output_col += 1

    # insert new rows, finish processing of inserted rows from the previous step
    output_row = 0
    new_output_grid = np.copy(output_grid)
    for row in range(input_height):
        output_row += 1
        if np.any(input_grid[row, :] != 0):
            output_col = 0
            for col in range(input_width):
              if input_grid[row][col] == 0:
                new_output_grid[output_row][output_col * 2] = 8
              if (col+1) < input_width:
                if input_grid[row][col+1] != 0:
                  new_output_grid[output_row][output_col * 2 + 1] = 8

              output_col+=1
            output_row += 1

    return new_output_grid
```