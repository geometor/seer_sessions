```python
"""
Transforms an input grid to an output grid based on the following rules:

1.  White (0) in the input becomes Green (3) in the output.
2.  Gray (5) in the input becomes:
    a. Red (2) if vertically adjacent to White (0).
    b. Yellow (4) if horizontally adjacent to White (0), but *not* vertically adjacent.
    c. Green (3) if diagonally adjacent to White (0), but *not* vertically or horizontally adjacent.
    d. Green (3) if not adjacent to White (0).
"""

import numpy as np

def get_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    for i in range(max(0, r - 1), min(rows, r + 2)):
        for j in range(max(0, c - 1), min(cols, c + 2)):
            if (i, j) != (r, c):  # Exclude the cell itself
                neighbors.append((i, j, grid[i][j]))
    return neighbors

def get_vertical_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c, grid[r - 1][c]))  # Up
    if r < rows - 1:
        neighbors.append((r + 1, c, grid[r + 1][c]))  # Down
    return neighbors

def get_horizontal_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    if c > 0:
        neighbors.append((r, c - 1, grid[r][c - 1]))  # Left
    if c < cols - 1:
        neighbors.append((r, c + 1, grid[r][c + 1]))  # Right
    return neighbors

def get_diagonal_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    if r > 0 and c > 0:
        neighbors.append((r - 1, c - 1, grid[r - 1][c - 1])) # Up-Left
    if r > 0 and c < cols - 1:
        neighbors.append((r - 1, c + 1, grid[r - 1][c + 1])) # Up-Right
    if r < rows - 1 and c > 0:
        neighbors.append((r + 1, c - 1, grid[r + 1][c - 1])) # Down-Left
    if r < rows - 1 and c < cols - 1:
        neighbors.append((r + 1, c + 1, grid[r + 1][c + 1])) # Down-Right
    return neighbors

def transform(input_grid):
    # initialize output_grid
    rows, cols = len(input_grid), len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # change output pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] == 0:
                output_grid[i][j] = 3
            elif input_grid[i][j] == 5:
                is_vertically_adjacent_to_0 = False
                is_horizontally_adjacent_to_0 = False
                is_diagonally_adjacent_to_0 = False

                for x, y, val in get_vertical_neighbors(input_grid, i, j):
                    if val == 0:
                        is_vertically_adjacent_to_0 = True
                        break  # Vertical adjacency takes precedence

                if not is_vertically_adjacent_to_0:
                    for x, y, val in get_horizontal_neighbors(input_grid, i, j):
                        if val == 0:
                            is_horizontally_adjacent_to_0 = True
                            break  # Horizontal adjacency takes precedence over diagonal

                if not is_vertically_adjacent_to_0 and not is_horizontally_adjacent_to_0:
                    for x, y, val in get_diagonal_neighbors(input_grid, i, j):
                        if val == 0:
                            is_diagonally_adjacent_to_0 = True
                            break

                if is_vertically_adjacent_to_0:
                    output_grid[i][j] = 2
                elif is_horizontally_adjacent_to_0:
                    output_grid[i][j] = 4
                elif is_diagonally_adjacent_to_0:
                    output_grid[i][j] = 3
                else:
                    output_grid[i][j] = 3  # Not adjacent to 0

    return output_grid
```