```python
"""
Transforms an input grid by propagating non-zero values from the last row upwards.
The last row's non-zero elements act as anchors. For each column, if the last row
has a non-zero value, the algorithm fills upwards, replacing zeros with the
first non-zero value encountered in the upper rows of that column.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Check if the anchor (last row element) is non-zero
        if input_grid[rows - 1, j] != 0:
            # Iterate upwards from the second-to-last row
            for i in range(rows - 2, -1, -1):
                #Find first non-zero value moving up the rows
                first_non_zero = 0
                for k in range(i, -1, -1):
                  if input_grid[k,j] != 0:
                    first_non_zero = input_grid[k,j]
                    break

                if output_grid[i,j] == 0:
                  output_grid[i,j] = first_non_zero
    return output_grid
```