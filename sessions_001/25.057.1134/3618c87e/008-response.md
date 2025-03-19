# 3618c87e • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to swap the positions of the blue (1) and gray (5) pixels in the input grid to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all blue (1) pixels.
    blue_coords = np.argwhere(input_grid == 1)

    # Find the coordinates of all gray (5) pixels.
    gray_coords = np.argwhere(input_grid == 5)
    
    # Swap colors based on input grid coordinates
    for coord in blue_coords:
        output_grid[coord[0], coord[1]] = 5
        
    for coord in gray_coords:
        output_grid[coord[0], coord[1]] = 1
    
    return output_grid
```
