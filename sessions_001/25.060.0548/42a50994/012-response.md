# 42a50994 • 012 • refine_coder

---
```python
"""
The transformation rule identifies and removes magenta (6) pixels from the input grid based on their spatial relationships with neighboring magenta pixels. Magenta pixels that are part of diagonal lines of 2 or more, or part of a 2x2 square, are preserved. Other magenta pixels are changed to white (0).
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonals=True):
    """Gets the neighbors of a cell, optionally including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not include_diagonals and (abs(i) + abs(j) != 1): #skip diag
                continue

            neighbor_row = row + i
            neighbor_col = col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def is_part_of_diagonal(grid, row, col):
    """Checks if a magenta pixel is part of a diagonal of 2 or more."""
    if grid[row, col] != 6:
        return False

    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        if grid[r,c] == 6: # found magenta neighbor
            #check for diag - must be diff of 1
            if abs(row-r) + abs(col - c) == 2:
                return True

    return False

def is_part_of_2x2_square(grid, row, col):
    """Checks if a magenta pixel is part of a 2x2 square."""
    if grid[row, col] != 6:
        return False

    rows, cols = grid.shape
    # Check for 2x2 square in all possible positions relative to current cell
    for i in range(-1, 1):
        for j in range(-1, 1):
            if 0 <= row + i < rows -1 and 0 <= col + j < cols - 1: # make sure starting corner is valid
                #check square
                if (grid[row + i,     col + j] == 6 and
                    grid[row + i + 1, col + j] == 6 and
                    grid[row + i,     col + j + 1] == 6 and
                    grid[row + i + 1, col + j + 1] == 6):
                    return True
    return False


def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the grid
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is magenta
            if input_grid[row, col] == 6:
                # if isolated, or not part of group - remove it
                if not is_part_of_2x2_square(input_grid, row, col) and not is_part_of_diagonal(input_grid, row, col):
                     output_grid[row, col] = 0
                #else keep

    return output_grid
```
