# 6c434453 • 006 • refine_coder

---
```python
"""
Identifies all 3x3 blue crosses (plus signs) in the input grid and transforms them to red,
regardless of their adjacency to other crosses.
"""

import numpy as np

def find_crosses(grid):
    """
    Identifies centers of 3x3 crosses (plus signs) of a specific color in the grid.
    """
    cross_centers = []
    rows, cols = grid.shape
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if (grid[r, c] == 1 and
                grid[r-1, c] == 1 and
                grid[r+1, c] == 1 and
                grid[r, c-1] == 1 and
                grid[r, c+1] == 1):
                cross_centers.append((r, c))
    return cross_centers

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    output_grid = np.copy(input_grid)

    # Find all blue crosses
    blue_cross_centers = find_crosses(input_grid)

    # Perform the replacement of the center and four arms for all crosses
    for r, c in blue_cross_centers:
        output_grid[r, c] = 2  # Center to red
        output_grid[r-1, c] = 2  # Top to red
        output_grid[r+1, c] = 2  # Bottom to red
        output_grid[r, c-1] = 2  # Left to red
        output_grid[r, c+1] = 2  # Right to red

    return output_grid
```
