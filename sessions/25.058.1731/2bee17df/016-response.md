# 2bee17df • 016 • example_3 • investigate_coder

---
```python
"""
Preserves azure and red pixels, and changes some white pixels to green based a recursive propagation rule. 
The transformation starts on row 6, where white cells adjacent to azure cells become green.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of valid neighbor coordinates for a given cell in the grid.
    """
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Create a set to track visited white pixels to avoid infinite loops
    visited = set()

    # Recursive function to change white pixels to green
    def propagate_green(row, col):
        if (row, col) in visited or output_grid[row, col] != 0:
            return
        visited.add((row, col))
        output_grid[row, col] = 3
        for nr, nc in get_neighbors(output_grid, row, col):
                propagate_green(nr, nc)

    # Iterate through row 6 (index 5) to find starting points for propagation
    for col in range(cols):
        if output_grid[5, col] == 0:
            neighbors = get_neighbors(output_grid, 5, col)
          
            for neighbor_row, neighbor_col in neighbors:
                if output_grid[neighbor_row,neighbor_col] == 8:
                    propagate_green(5,col)
                    break

    return output_grid
```
