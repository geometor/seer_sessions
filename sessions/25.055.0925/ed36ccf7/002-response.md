# ed36ccf7 • 002 • example_1 • investigate_coder

---
```python
"""
Swap the values of the first row and first column of a 2D grid. Specifically:
1. Identify the color of the top-left cell.
2. Set the first column of the output grid to the colors of the first row of the input.
3. Set the first row of the output grid to the colors of the first column of the input,
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
    
    # Swap the first row and first column
    # Except for the top-left element
    for i in range(1,rows):
        output_grid[i,0] = input_grid[0,i]
        output_grid[0,i] = input_grid[i,0]
    output_grid[0,0] = top_left_color


    return output_grid
```
