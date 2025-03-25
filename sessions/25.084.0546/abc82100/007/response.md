```python
"""
Transforms an input grid into an output grid based on a combination of color swaps and
positional/neighbor-based rules. The rules include:

1.  **Color Swaps:**
    *   If a pixel is color 2, it becomes color 1.
    *   If a pixel is color 6, it becomes color 7.
    *   If a pixel is color 7, it becomes color 6.

2.  **Conditional Transformations:**
    *   If a pixel is color 1 AND is adjacent to a pixel of color 2, it becomes color 2.
        *   If a pixel is color 1 and is not adjacent to a pixel of color 2, it becomes color 0.
    *   If a pixel is color 4:
        *   If the pixel is on the top, bottom, left, or right edge of the *entire grid*, it becomes 2.
        *   If a pixel of color '4' is not located on the outer edge of the grid, it will retain its color.
    *   If a pixel is color 8, it becomes color 0.

3.  **Object Removal**
    *    Objects of color 8 are removed.

4.  **Default:**
    *   If a pixel is color 0, it remains color 0.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell, including diagonals."""
    neighbors = []
    rows, cols = grid.shape
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i][j])
    return neighbors

def is_adjacent_to(grid, row, col, target_color):
    """Checks if a cell is adjacent to a cell of a specific color."""
    neighbors = get_neighbors(grid, row, col)
    return target_color in neighbors

def is_on_edge(grid, row, col):
    """Checks if a cell is on the edge of the grid."""
    rows, cols = grid.shape
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1

def transform(input_grid):
    # initialize output_grid with zeros, same dimensions as input.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # iterate through each cell of input_grid
    for i in range(rows):
        for j in range(cols):
            # Apply color mapping rules
            if input_grid[i][j] == 0:
                output_grid[i][j] = 0  # Keep 0 as 0
            elif input_grid[i][j] == 1:
                if is_adjacent_to(input_grid, i, j, 2):
                    output_grid[i][j] = 2  # 1 becomes 2 if adjacent to 2
                else:
                    output_grid[i][j] = 0 # 1 becomes 0 otherwise
            elif input_grid[i][j] == 2:
                output_grid[i][j] = 1  # 2 becomes 1
            elif input_grid[i][j] == 6:
                output_grid[i][j] = 7  # 6 becomes 7
            elif input_grid[i][j] == 7:
                output_grid[i][j] = 6  # 7 becomes 6
            elif input_grid[i][j] == 4:
                if is_on_edge(input_grid, i, j):
                    output_grid[i][j] = 2 # 4 becomes 2 if on edge
                else:
                    output_grid[i][j] = 4 # Otherwise, 4 remains unchanged
            elif input_grid[i][j] == 8:
                output_grid[i][j] = 0  # 8 becomes 0

    return output_grid
```
