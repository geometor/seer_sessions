# d90796e8 • 012 • refine_coder

---
```python
"""
1.  Identify all 1x1 regions (single pixels) of color green (3).
2.  Change the color of these identified green pixels to azure (8).
3.  Identify all 1x1 regions (single pixels) that are the color red (2).
4.  Change the color of the identified red pixels to white (0).
5.  Preserve all other pixels in their original state and positions.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified color change rules,
    specifically targeting 1x1 regions of green and red."""
    output_grid = np.copy(input_grid)  # Create a copy to modify

    # Iterate through each cell of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the current pixel is part of a 1x1 region
            if is_1x1_region(input_grid, i, j):
                # Change green (3) to azure (8)
                if output_grid[i, j] == 3:
                    output_grid[i, j] = 8
                # Change red (2) to white (0)
                elif output_grid[i, j] == 2:
                    output_grid[i, j] = 0

    return output_grid

def is_1x1_region(grid, i, j):
    """Checks if the pixel at (i, j) is a 1x1 region of its color."""
    color = grid[i, j]
    
    # Check boundaries
    min_row = max(0, i - 1)
    max_row = min(grid.shape[0] - 1, i + 1)
    min_col = max(0, j - 1)
    max_col = min(grid.shape[1] - 1, j + 1)

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if (row != i or col != j) and grid[row, col] == color:
                return False  # Found a neighbor with the same color
    return True  # No neighbors with the same color

```
