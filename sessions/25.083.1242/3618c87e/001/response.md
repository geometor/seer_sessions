```python
"""
Copies the input grid to the output grid, except for blue (1) pixels. 
Blue pixels are changed to white (0) in all rows except the last one.
On the last row, any blue pixel is changed to gray and any gray pixel is
changed to blue.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # If not the last row and the cell is blue (1), change it to white (0)
            if i != rows - 1 and input_grid[i, j] == 1:
                output_grid[i, j] = 0
            # For the last row, swap 1's and non-1's based on the locations
            elif i == rows - 1:
                if input_grid[i,j] == 1:
                    output_grid[i,j] = 5
                elif input_grid[i-1,j] == 1 and input_grid[i,j] != 1:
                    output_grid[i,j] = 1

    return output_grid.tolist()
```
