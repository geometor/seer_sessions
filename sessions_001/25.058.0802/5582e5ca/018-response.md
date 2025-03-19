# 5582e5ca • 018 • refine_coder

---
```python
"""
1.  **Check for Uniform Input:** If the input grid consists of only one color, the output grid is identical to the input.

2.  **Identify a Predominant, Adjacent Color, and Fill:** Examine the input grid. If a color appears in at least two adjacent positions (horizontally, vertically, or diagonally) anywhere in the grid, create an output grid of the same dimensions and fill it entirely with that color.

3.  **Otherwise, Identity**: If there is no uniform input color (step 1) and there aren't at least 2 adjacent pixels (step 2), the output grid is identical to the input.
"""

import numpy as np

def is_uniform(grid):
    """Checks if the grid has only one color."""
    return np.all(grid == grid[0, 0])

def find_adjacent_color(input_grid):
    """
    Finds a color that appears in at least two adjacent positions (horizontally, vertically, or diagonally).
    """
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            # Check horizontal
            if c + 1 < cols and input_grid[r, c + 1] == color:
                return color
            # Check vertical
            if r + 1 < rows and input_grid[r + 1, c] == color:
                return color
            # Check diagonal (top-left to bottom-right)
            if r + 1 < rows and c + 1 < cols and input_grid[r + 1, c + 1] == color:
                return color
            # Check diagonal (top-right to bottom-left)
            if r + 1 < rows and c - 1 >= 0 and input_grid[r + 1, c - 1] == color:
                return color
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Check for Uniform Input
    if is_uniform(input_grid):
        return output_grid

    # Identify a Predominant, Adjacent Color, and Fill
    target_color = find_adjacent_color(input_grid)
    if target_color is not None:
        output_grid[:] = target_color
        return output_grid

    # Otherwise, Identity
    return output_grid
```
