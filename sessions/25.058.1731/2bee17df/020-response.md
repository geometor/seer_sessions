# 2bee17df • 020 • refine_coder

---
```python
"""
Preserves azure and red pixels, and changes some white pixels to green based on a recursive propagation rule.
The transformation starts on the row immediately below any azure pixel if the pixel below is white.
Or, it starts on the row immediately above a red pixel if the pixel above is white.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of valid neighbor coordinates for a given cell in the grid,
    including diagonals.
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

    # Iterate through the grid to find starting points for propagation
    for row in range(rows):
        for col in range(cols):
            # Check for azure pixels and propagation below
            if output_grid[row, col] == 8:  # Found an azure pixel
                if row + 1 < rows and output_grid[row + 1, col] == 0:
                    propagate_green(row + 1, col)
            #check for red pixels and propagation above
            elif output_grid[row,col] == 2: # Found a red pixel
                if row - 1 >= 0 and output_grid[row-1, col] == 0:
                    propagate_green(row -1, col)

    return output_grid
```
