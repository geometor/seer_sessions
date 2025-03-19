# 83302e8f • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify the Azure Shape:** Locate the connected shape formed by azure (8) pixels. This shape consists of diagonal lines.

2.  **Analyze White Pixel Adjacency:** Examine the white (0) pixels adjacent to the azure shape.

3.  **Conditional Color Change:**
    *   If a white pixel is directly above or below an azure pixel, change its color to green (3).
    *   If a white pixel is directly to the left or right of an azure pixel, change its color to yellow (4).
    * If a white pixel is diagonally adjacent, leave it unchanged.

4.  The azure shape's color is preserved, so no changes happen to its colors.
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
