# ed36ccf7 • 004 • refine_coder

---
```python
"""
Swap the values of the first row and first column of a 2D grid. Specifically:
1. Identify the color of the top-left cell.
2. Copy elements of the first row of the input grid to the first column of the output grid.
3. Copy elements of the first column of the input grid to the first row of the output grid,
   making sure that the top-left cell keeps its original color.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape
    
    # Store original top-left cell color
    top_left_color = input_grid[0, 0]
    
    # Determine the minimum dimension for swapping to handle rectangular arrays
    min_dim = min(rows, cols)
    
    # copy first row to first column
    for i in range(1,rows):
        if i < cols:
           output_grid[i,0] = input_grid[0,i]

    # copy first column to first row
    for i in range(1,cols):
        if i < rows:
            output_grid[0,i] = input_grid[i,0]

    # restore top left
    output_grid[0,0] = top_left_color


    return output_grid
```
