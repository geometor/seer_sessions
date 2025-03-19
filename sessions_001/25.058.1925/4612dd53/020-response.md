# 4612dd53 • 020 • refine_coder

---
```python
"""
1.  **Identify Blue Pixels:** Locate all pixels with the color blue (value 1) in the input grid.
2.  **Identify Adjacent Pixels:** For each blue pixel, identify its adjacent pixels. Adjacent pixels are those directly touching the blue pixel horizontally, vertically, or diagonally.
3.  **Change Neighbor Color:** Change the color of each adjacent pixel to red (value 2) *unless* the adjacent pixel is also blue.
4. **Preserve Blue**: All the blue pixels retain their input color.
"""

import numpy as np

def get_neighbors_diag(grid, row, col):
    """Gets the neighbors of a cell (up, down, left, right, and diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Skip the cell itself
            neighbor_row, neighbor_col = row + i, col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)  # Start with a copy of the input
    rows, cols = input_grid.shape

    # Iterate through each cell in the input grid
    for row in range(rows):
        for col in range(cols):
            # Check if current cell is blue
            if input_grid[row, col] == 1:
                # Get all adjacent neighbors (including diagonals)
                neighbors = get_neighbors_diag(input_grid, row, col)
                # Change the color of all non-blue neighbors to red.
                for n_row, n_col in neighbors:
                    if input_grid[n_row,n_col] != 1:
                         output_grid[n_row, n_col] = 2
            
    return output_grid
```
