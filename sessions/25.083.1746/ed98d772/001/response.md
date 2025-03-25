```python
"""
The input grid is expanded to double its size in both dimensions. 
Each row and column from the original grid is doubled to create a matrix,
then, this is used as the blueprint to create the whole output by translating
the positions.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with zeros, double the size of input_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # double the values from the original positions to create a new grid
    doubled_grid = np.zeros((rows, cols*2), dtype=int)    
    for i in range(rows):
      for j in range(cols):
        doubled_grid[i, 2 * j] = input_grid[i,j]
        doubled_grid[i, 2* j + 1] = input_grid[i,j]

    # Create the output using the double matrix
    for i in range(rows):
      for j in range(cols*2):
        output_grid[i, j] = doubled_grid[i,j]
        output_grid[i + rows, j] = doubled_grid[i,j]


    return output_grid
```