# 234bbc79 • 004 • example_1 • investigate_coder

---
```python
"""
Transforms an input grid into an output grid based on the following rules:
1. Grey (5) pixels are replaced based on their adjacency.
    - Replaced by white (0) if adjacent to white (0).
    - Replaced by blue (1) if adjacent to blue (1).
2. Other colors (red (2), blue (1), white (0)) remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the values of the neighbors of a cell."""
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
                if all(n == 0 or n == 5 for n in neighbors):
                    output_grid[i,j] = 0
                elif 1 in neighbors:
                    output_grid[i,j] = 1
    
    return output_grid
```

