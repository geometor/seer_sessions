```python
"""
Transforms a grid by replacing 5s in the last row with 1s, based on the positions of 1s in the third row.
The fourth row has 5s if the third row is non-zero at same position.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Get the number of rows and columns
    rows, cols = input_grid.shape
    
    # Maintain the first two rows as all zeros
    output_grid[:2, :] = 0

    # create row four
    for j in range(cols):
      if input_grid[2,j] != 0:
        output_grid[3,j] = 5

    # Transform Row 5 based on values in row 3
    for j in range(cols):
        if input_grid[2, j] == 1:
            output_grid[rows - 1, j] = 1
        else:
            output_grid[rows-1, j] = 5  # Keep as 5 if not 1 in row_3

    return output_grid
```
