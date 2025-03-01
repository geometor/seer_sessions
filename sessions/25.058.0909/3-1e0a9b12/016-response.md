# 3-1e0a9b12 • 016 • refine_coder

---
```python
"""
Stacks non-zero pixels in each column at the bottom of the grid, preserving their original vertical order within the column.
"""

import numpy as np

def get_nonzero_cells_by_column(grid):
    """Finds and returns non-zero cells, grouped by column and sorted by row within each column."""
    columns = {}
    for c in range(grid.shape[1]):
        columns[c] = []
        for r in range(grid.shape[0]):
            if grid[r, c] != 0:
                columns[c].append((r, c, grid[r, c]))
    return columns

def transform(input_grid):
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)

    # Get non-zero cells grouped by column and sorted by original row.
    nonzero_cells_by_column = get_nonzero_cells_by_column(input_grid)

    # Iterate through each column.
    for col, cells in nonzero_cells_by_column.items():
        # Start placing cells from the bottom row.
        current_row = input_grid.shape[0] - 1
        # Place each cell in the column, moving upwards.
        for _, _, value in reversed(cells):  # Reverse to stack from bottom
            output_grid[current_row, col] = value
            current_row -= 1 # move to the row above

    return output_grid
```
