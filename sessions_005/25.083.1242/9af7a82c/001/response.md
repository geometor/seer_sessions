```python
"""
The input grid is transformed into the output grid by taking the columns of the input, reversing their order, and placing them as the rows of the output grid.
Zeros (0) are then used to fill the output to the correct width (input height) and correct height (input width plus two).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = input_width + 2
    output_width = input_height
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    # iterate through columns in reverse order
    col_index = 0
    for j in range(input_width - 1, -1, -1):
      # copy the column to output grid
      for i in range(input_height):
        output_grid[col_index][i] = input_grid[i][j]
      col_index += 1

    return output_grid.tolist()
```