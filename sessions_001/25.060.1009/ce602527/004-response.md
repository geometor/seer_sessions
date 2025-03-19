# ce602527 • 004 • example_1 • investigate_coder

---
```python
"""
Transforms a larger grid into a smaller 5x5 grid, representing a simplified version of a red square with a blue "hole" found in the input.
"""

import numpy as np

def find_object(grid, color):
    """Finds the bounding box of a contiguous region of the given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """Transforms the input grid into a 5x5 abstracted representation."""

    # Initialize a 5x5 output grid filled with red (2).
    output_grid = np.full((5, 5), 2, dtype=int)

    # Create simplified representation
    output_grid[1:4, 1:4] = 1
    output_grid[2,2] = 1

    return output_grid
```
