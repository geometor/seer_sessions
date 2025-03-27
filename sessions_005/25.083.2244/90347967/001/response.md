```python
"""
The task involves transforming an input grid into an output grid.
The transformation appears to be a reversal of the order of cells, and some shifting.
1.  Reverse and Shift: Create the output grid by putting input cells in reverse order, bottom right cell be the same as input grid's upper left cell.
2.  Shift each row to the right until non-white (0) cells are right aligned
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Reverse the input grid and shift the non zero to the right
    reversed_grid = np.flip(input_grid)
    
    #shift each row of the reversed grid
    for i in range(rows):
      row_values = reversed_grid[i]
      non_zero_values = row_values[row_values != 0]
      num_zeros = len(row_values) - len(non_zero_values)
      new_row = np.concatenate((np.zeros(num_zeros), non_zero_values))
      output_grid[i] = new_row

    return output_grid.tolist()
```