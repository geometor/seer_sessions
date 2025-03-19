# 6a1e5592 • 002 • example_2 • investigate_coder

---
```python
"""
The transformation identifies a region of interest at the top of the grid, primarily defined by the presence of red and white pixels. Within this region, it changes white (0) pixels and gray(5) to blue (1), while preserving red (2) pixels.  The rest of the grid remains unchanged.
"""

import numpy as np

def find_region_of_interest(grid):
    """
    Finds the region of interest based on red and white pixels.
    """
    max_row = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 2 or grid[r,c] == 0:
                if r > max_row:
                   max_row = r
    return max_row + 1

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the Region of Interest
    region_end_row = find_region_of_interest(input_grid)

    # 2. Conditional Replacement within the region
    for r in range(min(region_end_row, rows)):  # Ensure we don't go out of bounds
        for c in range(cols):
            if output_grid[r, c] == 0 or output_grid[r,c] == 5:
                output_grid[r, c] = 1

    # 3. Preserve Lower Region (already handled by copying the input_grid initially)

    return output_grid
```
