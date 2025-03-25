```python
"""
The transformation identifies gray (5) objects in the input grid and fills
internal and adjacent "empty" (white, 0) spaces with azure (8) based on the
number of neighboring gray pixels.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """
    Get the valid neighbors of a cell in the grid.
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def count_gray_neighbors(grid, r, c):
    """
    Count the number of gray (5) neighbors around a cell.
    """
    neighbors = get_neighbors(grid, r, c)
    count = 0
    for nr, nc in neighbors:
        if grid[nr, nc] == 5:
            count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is white (0)
            if input_grid[r, c] == 0:
                # Count gray neighbors
                gray_count = count_gray_neighbors(input_grid, r, c)

                # Apply fill rule based on observation (different thresholds
                # observed in examples). Use a threshold >= 2 to cover both cases,
                # but note potential overfilling
                if gray_count >= 2:
                     output_grid[r, c] = 8  # Fill with azure

    return output_grid
```
