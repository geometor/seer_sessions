```python
"""
1.  **Identify the Separator:** Find the horizontal line of grey (5) pixels in the input grid.

2.  **Copy Above:** Copy all rows of the input grid *above* the grey line to the output grid.

3. **Locate non-zeros**: locate any non zero integers in the rows beneath the grey line.

4. **Insert**: any time a non-zero integer is found, insert that integer into the corresponding column of the first few rows of the output. Non-zeros located further down the input grid are placed in higher rows of the output grid.

5. **Zero Row Deletion**: Delete any all-zero rows in the result.
"""

import numpy as np

def find_grey_line(grid):
    # Find the row index of the grey line (all 5s).
    for i, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            return i
    return -1  # Grey line not found

def transform(input_grid):
    input_grid = np.array(input_grid)
    grey_line_index = find_grey_line(input_grid)
    output_grid = []

    # Copy rows above the grey line
    for i in range(grey_line_index):
        output_grid.append(list(input_grid[i]))

    # Find non-zero elements below the grey line and insert
    insert_row = grey_line_index -1
    for i in range(grey_line_index+1,len(input_grid)):
      for j in range(len(input_grid[0])):
        if input_grid[i][j] !=0:
          if insert_row >= 0:
            output_grid[insert_row][j] = input_grid[i][j]
      insert_row -= 1
    
    #delete any all-zero rows
    output_grid = [row for row in output_grid if any(x != 0 for x in row)]

    return output_grid
```