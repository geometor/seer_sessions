# dbc1a6ce • 026 • refine_coder

---
```python
"""
Iterate through each pixel of the input grid.
Identify white pixels (value 0).
For each white pixel, check its eight neighboring pixels (including diagonals).
If any of the neighboring pixels are blue (value 1), change the color of the white pixel to azure (value 8).
Pixels that are not white or are not adjacent to a blue pixel remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns the neighbors of a pixel, the 8 pixels surrounding it
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    # Initialize the output grid with the same values as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the grid.
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is white.
            if input_grid[row, col] == 0:
                # Get the neighbors of the current pixel
                neighbors = get_neighbors(input_grid, row, col)

                # Check if any neighbor is blue.
                if 1 in neighbors:
                    # Change the white pixel to azure.
                    output_grid[row, col] = 8

    return output_grid
```
