# 1190e5a7 • 010 • example_2 • investigate_coder

---
```python
"""
Extracts the top-left subgrid of 1s from the input grid, stopping before the first occurrence of 8 in any row or column.
"""

import numpy as np

def find_first_occurrence(grid, value):
    """Finds the first row and column index where the given value appears."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == value:
                return r, c
    return rows, cols  # Return grid size if value not found


def transform(input_grid):
    """
    Extracts a sub-grid from the input, stopping before the first 8.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Find the first occurrence of 8
    first_8_row, first_8_col = find_first_occurrence(input_grid, 8)

    # Extract the subgrid
    output_grid = input_grid[:first_8_row, :first_8_col]

    return output_grid.tolist()
```
