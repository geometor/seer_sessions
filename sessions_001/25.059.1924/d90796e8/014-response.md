# d90796e8 • 014 • refine_coder

---
```python
"""
1.  **Identify Isolated Pixels:** Examine each pixel in the input grid. A pixel is considered "isolated" if none of its immediate neighbors (up, down, left, right, and diagonals) have the same color as the pixel itself.
2.  **Transform Green:** If an isolated pixel is green (color 3), change its color to azure (color 8).
3.  **Transform Red:** If an isolated pixel is red (color 2), change its color to white (color 0).
4.  **Preserve Other Pixels:** All other pixels that are not isolated, or are not green or red, should remain unchanged in both color and position.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by changing isolated green pixels to azure and isolated red pixels to white."""
    output_grid = np.copy(input_grid)  # Create a copy to modify

    # Iterate through each pixel of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the current pixel is isolated
            if is_isolated(input_grid, i, j):
                # Change isolated green (3) to azure (8)
                if output_grid[i, j] == 3:
                    output_grid[i, j] = 8
                # Change isolated red (2) to white (0)
                elif output_grid[i, j] == 2:
                    output_grid[i, j] = 0

    return output_grid

def is_isolated(grid, i, j):
    """Checks if the pixel at (i, j) is isolated (no neighbors have the same color)."""
    color = grid[i, j]
    
    # Check boundaries to avoid index errors
    min_row = max(0, i - 1)
    max_row = min(grid.shape[0] - 1, i + 1)
    min_col = max(0, j - 1)
    max_col = min(grid.shape[1] - 1, j + 1)

    # Iterate through neighbors, including diagonals
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if (row != i or col != j) and grid[row, col] == color:
                return False  # Found a neighbor with the same color, not isolated
    return True  # No neighbors with the same color, pixel is isolated
```
