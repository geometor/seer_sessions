# 83302e8f • 007 • refine_coder

---
```python
"""
1.  Examine the input grid: Iterate through each cell of the input grid.
2.  Check for White Cells: For each cell, check if its color is white (0).
3. Check for Azure Neighbors (only if the current cell is white): If the cell is white, examine its immediate neighbors (up, down, left, right, and diagonals).
4.  Conditional Color Change:
    *   If a neighbor directly above or below the white cell is azure (8), change the white cell's color to green (3).
    *   If a neighbor directly to the left or right of the white cell is azure (8), change the white cell's color to yellow (4).
5. No white cells condition: If no white cells are present in the input grid, return the original grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell, including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row, neighbor_col = row + i, col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check if there are any white cells in the grid
    if 0 not in input_grid:
        return output_grid

    # Iterate through each cell in the grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current cell is white (0)
            if input_grid[row, col] == 0:
                neighbors = get_neighbors(input_grid, row, col)
                for n_row, n_col in neighbors:
                    # Check for directly above/below (green) or left/right (yellow) azure neighbors
                    if input_grid[n_row, n_col] == 8:
                        if n_row == row:  # Left or Right
                            output_grid[row, col] = 4 # yellow
                            break  # Apply only one transformation
                        elif n_col == col:  # Above or Below
                            output_grid[row, col] = 3  # green
                            break  # Apply only one transformation

    return output_grid
```
