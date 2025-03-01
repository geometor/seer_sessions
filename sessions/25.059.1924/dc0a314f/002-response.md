# dc0a314f • 002 • example_3 • investigate_coder

---
```python
"""
The transformation extracts a 5x5 subgrid from the input grid. The subgrid is
centered at a specific offset relative to the input grid's center.
"""

import numpy as np

def get_center(grid):
    """Calculates the center coordinates of a grid."""
    height, width = grid.shape
    center_y = height // 2
    center_x = width // 2
    return center_y, center_x

def transform(input_grid):
    """
    Extracts a 5x5 subgrid from the input grid, centered at a consistent offset.
    """
    input_grid = np.array(input_grid)
    center_y, center_x = get_center(input_grid)

    # Determine the offset from center to define starting point for output grid
    # offsets determined by examining first and second input/output examples
    offset_y = 3
    offset_x = 3

    start_y = center_y - 2 + offset_y
    start_x = center_x - 2 + offset_x

   
    # Extract the 5x5 subgrid
    output_grid = input_grid[start_y:start_y+5, start_x:start_x+5]
    
    return output_grid.tolist()
```
