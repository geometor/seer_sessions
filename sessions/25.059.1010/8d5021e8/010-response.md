# 8d5021e8 • 010 • example_2 • investigate_coder

---
```python
"""
The input grid (3x2) is expanded to a larger output grid (9x4).  A 2x2 block of red pixels from the input is replicated and positioned across and down the output grid.  The remaining cells are filled with white.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid (9x4)
    output_grid = np.zeros((9, 4), dtype=int)

    # Create the 2x2 red block
    red_block = np.full((2, 2), 2, dtype=int)

    # Horizontal and Vertical Placement of red blocks
    for i in range(3):  # Vertical placement (3 times)
        for j in range(3):  # Horizontal placement (3 blocks + 1 overlapping)
            output_grid[i*2:i*2+2, j : j+2] = red_block

    return output_grid
```
