```python
"""
Transforms an input grid by propagating non-zero values from the last row
upwards in their respective columns, replacing zeros.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column.
    for j in range(cols):
        # Get the value from the last row in the current column.
        last_row_value = output_grid[rows - 1, j]

        # If the value in the last row is non-zero, propagate it upwards.
        if last_row_value != 0:
            # Iterate upwards from the second-to-last row.
            for i in range(rows - 2, -1, -1):
                # If the current cell is zero, replace it with the last row's value.
                if output_grid[i, j] == 0:
                    output_grid[i, j] = last_row_value
                else:
                  continue # if we encounter a non-zero value higher, stop filling

    return output_grid
```
