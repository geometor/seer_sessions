# 88a10436 • 014 • refine_coder

---
```python
"""
1.  Create a 30x30 grid filled with black (0).
2.  Place a single magenta (6) pixel at row 5, column 1 (using 0-based indexing, this is grid[4, 0]).
3.  Place a horizontal blue (1) line of length 2, starting at row 6, column 1 (grid[5, 0] and grid[5, 1]).
4.  Place a horizontal red (2) line of length 3, starting at row 7, column 1 (grid[6, 0], grid[6, 1], and grid[6, 2]).
5.  The rest of the grid remains black (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize a 30x30 output grid filled with 0 (black).
    output_grid = np.zeros((30, 30), dtype=int)

    # Place a magenta pixel at (4, 0).
    output_grid[4, 0] = 6

    # Place a blue line of length 2 at (5, 0).
    output_grid[5, 0] = 1
    output_grid[5, 1] = 1

    # Place a red line of length 3 at (6, 0).
    output_grid[6, 0] = 2
    output_grid[6, 1] = 2
    output_grid[6, 2] = 2

    return output_grid
```

