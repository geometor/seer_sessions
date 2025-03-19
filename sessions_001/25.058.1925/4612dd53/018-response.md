# 4612dd53 • 018 • refine_coder

---
```python
"""
1.  **Identify Blue Regions:** Locate all contiguous regions of blue (1) pixels within the input grid.
2.  **Identify other pixels:** Note the location and color of all non-blue pixels
3.  **Leak Red:** For every pixel that is *adjacent* (horizontally, vertically, or diagonally) to a blue pixel, change its color to red (2) in the output grid.
4. **Preserve Blue**: The blue pixels retain their original color and location.
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
