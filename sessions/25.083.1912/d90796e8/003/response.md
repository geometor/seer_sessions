```python
"""
If a green (3) pixel is adjacent (orthogonally or diagonally) to a red (2) pixel,
the green pixel is changed to azure (8). All other colors are unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Gets the neighbors of cell.
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row = row + i
            neighbor_col = col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid: If a green (3) pixel is adjacent to a red (2) pixel,
    change the green pixel to azure (8).
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            # Only proceed if the current pixel is green (3)
            if input_grid[row, col] == 3:
                neighbors = get_neighbors(input_grid, row, col)
                for neighbor_row, neighbor_col in neighbors:
                    # If a neighbor is red (2), change the current (green) pixel to azure (8)
                    if input_grid[neighbor_row, neighbor_col] == 2:
                        output_grid[row, col] = 8
                        break  # Once changed, no need to check other neighbors

    return output_grid
```