```python
"""
Extracts a 2x2 subgrid from the input grid. The subgrid is located in the upper-left quadrant and is identified by a 2x2 pattern of non-zero values, surrounded by zeros.
"""

import numpy as np

def find_subgrid(input_grid):
    """Finds the 2x2 subgrid within the input grid."""
    rows, cols = input_grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = input_grid[r:r+2, c:c+2]
            if np.all(subgrid != 0) and is_bordered_by_zeros(input_grid, r, c):
              if subgrid[0,0] != subgrid[1,0] and subgrid[0,1] != subgrid[1,1]:
                return r, c
    return None, None

def is_bordered_by_zeros(input_grid, r, c):
    """Checks if the 2x2 subgrid at (r, c) is bordered by zeros."""
    rows, cols = input_grid.shape

    # Check top border
    if r > 0 and np.any(input_grid[r-1, c:c+2] != 0):
        return False

    # Check bottom border
    if r < rows - 2 and np.any(input_grid[r+2, c:c+2] != 0):
        return False

    # Check left border
    if c > 0 and np.any(input_grid[r:r+2, c-1] != 0):
        return False
    
    # Check Right border
    if c < cols-2 and np.any(input_grid[r:r+2,c+2] !=0):
        return False

    return True

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Find the starting coordinates of the subgrid
    r, c = find_subgrid(input_grid)

    # Initialize output_grid as an empty 2x2 array.
    output_grid = np.zeros((2,2), dtype=int)
    
    if r is not None and c is not None:
      # Extract subgrid first columns
      output_grid = input_grid[r:r+2, c:c+2].copy()

    return output_grid.tolist()
```