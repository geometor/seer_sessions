# beb8660c • 014 • example_3 • investigate_coder

---
```python
"""
The transformation is a 90-degree clockwise rotation of the top-left 2x2 subgrid, while keeping the bottom row unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # rotate the top-left 2x2 subgrid clockwise by 90 degrees
    # cell(0,0) moves to cell(1,0)
    output_grid[1][0] = input_grid[0][0]
    # cell(1,0) moves to cell(1,1)
    output_grid[1][1] = input_grid[1][0]
    # cell(1,1) moves to cell (0,1)
    output_grid[0][1] = input_grid[1][1]
    # cell(0,1) moves to cell(0,0)
    output_grid[0][0] = input_grid[0][1]
    
    return output_grid
```
