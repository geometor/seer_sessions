# f76d97a5 • 018 • refine_coder

---
```python
"""
Replaces '5' with '0' in a grid, unless the '5' is diagonally adjacent to a '9', in which case the '5' remains unchanged.
"""

import numpy as np

def get_diagonals(grid, row, col):
    """
    Returns a list of the values of the diagonal neighbors of a cell.
    """
    rows, cols = grid.shape
    diagonals = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            if 0 <= row + i < rows and 0 <= col + j < cols:
                diagonals.append(grid[row + i, col + j])
    return diagonals

def transform(input_grid):
    """
    Transforms the input grid according to the rule.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for row in range(rows):
        for col in range(cols):
            # Check if the cell's value is 5
            if input_grid[row, col] == 5:
                # Get the values of the diagonal neighbors
                diagonals = get_diagonals(input_grid, row, col)
                # Check if any diagonal neighbor is 9
                if any(d == 9 for d in diagonals):
                    #If true, leave value at 5
                    output_grid[row,col] = 5
                else:
                    # If not, change the cell's value to 0
                    output_grid[row, col] = 0

    return output_grid
```
