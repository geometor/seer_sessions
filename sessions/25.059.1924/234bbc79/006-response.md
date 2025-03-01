# 234bbc79 • 006 • refine_coder

---
```python
"""
Transforms an input grid into an output grid based on the following rules:

1.  **Initialization:** The output grid starts as a copy of the input grid.
2.  **Grey Pixel Transformation:** Iterate through each cell of the grid. If a cell is grey (5):
    *   Examine its immediate neighbors (including diagonals).
    *   If *any* neighbors are blue (1), change the grey pixel to blue (1).
    *   If all neighbors are grey (5) or white (0), change the grey to white (0)
    *   Otherwise, leave the grey pixel unchanged.
3.  **Other Colors:** Pixels that are not grey (5) in the input grid remain unchanged in the output grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the values of the neighbors of a cell, including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell
    for i in range(rows):
        for j in range(cols):
            # Check if the cell is grey (5)
            if output_grid[i, j] == 5:
                neighbors = get_neighbors(output_grid, i, j)
                # Replace based on neighbors
                if 1 in neighbors:
                    output_grid[i, j] = 1  # Change to blue if any neighbor is blue
                elif all(n == 5 or n == 0 for n in neighbors):
                  output_grid[i,j] = 0

    return output_grid
```
