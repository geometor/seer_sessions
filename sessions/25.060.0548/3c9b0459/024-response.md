# 3c9b0459 • 024 • refine_coder

---
```python
"""
1.  **Identify** the uppermost non-zero pixel in the input grid.
2.  **Identify** the lowermost non-zero pixel in the input grid.
3.  **If** the uppermost and lowermost pixel are not the same, **Swap** their positions in the output grid.
4. **If** the uppermost and lowermost pixel are the same, do nothing (no-op).
5.  **All other pixels** in the grid remain in their original positions.
"""

import numpy as np

def find_uppermost_nonzero(grid):
    """Finds the row and column index of the uppermost non-zero pixel."""
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                return r, c
    return None  # Return None if no non-zero pixel is found

def find_lowermost_nonzero(grid):
    """Finds the row and column index of the lowermost non-zero pixel."""
    for r in range(len(grid) - 1, -1, -1):
        for c in range(len(grid[0])):
            if grid[r][c] != 0:
                return r, c
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find uppermost and lowermost non-zero pixels
    uppermost = find_uppermost_nonzero(input_grid)
    lowermost = find_lowermost_nonzero(input_grid)
    
    # change output pixels 
    if uppermost is not None and lowermost is not None and uppermost != lowermost :
      # Swap their positions
      output_grid[uppermost[0], uppermost[1]], output_grid[lowermost[0], lowermost[1]] = \
      output_grid[lowermost[0], lowermost[1]], output_grid[uppermost[0], uppermost[1]]

    return output_grid
```
