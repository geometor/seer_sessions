# 28e73c20 • 008 • example_1 • investigate_coder

---
```python
"""
Transforms a 6x6 grid of white pixels (0) into a grid with a green border (3) and a white cross inside.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = output_grid.shape
    
    # Change all pixels on the outer border to green (3)
    for i in range(rows):
        for j in range(cols):
            if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                output_grid[i, j] = 3
            
    # Create a plus pattern of white pixels inside the frame.
    # Iterate, excluding the border to create white pixels.
    for i in range(1, rows -1):
        output_grid[1,i] = 0
        output_grid[i,1] = 0

    return output_grid
```
