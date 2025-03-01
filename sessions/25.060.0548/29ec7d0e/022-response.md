# 29ec7d0e • 022 • example_4 • investigate_coder

---
```python
"""
Removes zeros from the input grid based on their surrounding neighbors. A zero is removed if all of its eight neighbors are non-zero.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 8 neighboring pixels of a given cell (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    """Transforms the input grid by removing zeros based on neighbor context."""
    input_grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy of the input
    rows, cols = input_grid.shape

    # Iterate through each cell in the grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current cell is a zero
            if input_grid[row, col] == 0:
                neighbors = get_neighbors(input_grid, row, col)
                # Remove the zero if surrounded by non zeros
                if all(neighbor != 0 for neighbor in neighbors):
                     output_grid[row,col] = input_grid[row,col] # keep
                if all(neighbor == 1 for neighbor in neighbors):
                    output_grid[row,col] = 1 # all ones, change to one.
                # keep the zeros.

    return output_grid.tolist() # return as list
```
