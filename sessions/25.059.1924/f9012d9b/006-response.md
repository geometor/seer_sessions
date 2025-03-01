# f9012d9b • 006 • refine_coder

---
```python
"""
The transformation rule identifies the rightmost vertical object in the input grid
that extends to the bottom row. The output is a 2x2 grid where the bottom-right
cell is the color of that object and the rest of the cells are white.
"""

import numpy as np

def find_rightmost_vertical_object(grid):
    """
    Finds the rightmost vertical object in the grid that extends to the bottom row.
    Returns the color of the object or 0 if no such object exists.
    """
    rows, cols = grid.shape
    for j in range(cols - 1, -1, -1):  # Iterate columns from right to left
        for i in range(rows - 1, 0, -1):  # Iterate rows from bottom up (skip last row)
            if grid[i, j] != 0 and grid[i, j] == grid[i - 1, j]:
                return grid[i, j]  # Found a vertical object
    return 0  # No vertical object found


def transform(input_grid):
    """
    Transforms the input grid according to the rule.
    """
    # Find the dominant color of the rightmost vertical object
    dominant_color = find_rightmost_vertical_object(input_grid)

    # Create a 2x2 output grid filled with white
    output_grid = np.zeros((2, 2), dtype=int)

    # Set the bottom-right cell to the dominant color
    output_grid[1, 1] = dominant_color

    return output_grid
```
