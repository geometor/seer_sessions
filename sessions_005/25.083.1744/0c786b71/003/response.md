```python
"""
The output grid is twice the size of the input grid in both dimensions. 
The columns of the input grid are replicated in the output grid, maintaining their original order. 
Each column from the input grid appears twice in the output grid, adjacent to each other.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of input grid
    input_height, input_width = input_grid.shape
    
    # Initialize output grid with doubled dimensions
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid columns from left to right
    for j in range(input_width):
      input_col = input_grid[:, j]
      
      # Copy the input column to two adjacent columns in the output grid
      output_grid[:input_height, j*2] = input_col
      output_grid[:input_height, j*2+1] = input_col
      output_grid[input_height:, j*2] = input_col
      output_grid[input_height:, j*2+1] = input_col

    return output_grid
```