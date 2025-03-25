```python
"""
Transforms an input grid to an output grid based on the following rules:

1.  White (0) in the input becomes Green (3) in the output.
2.  Gray (5) in the input becomes:
    a. Red (2) if vertically adjacent to White (0).
    b. Yellow (4) if horizontally adjacent to White (0).
    c. Green (3) if diagonally adjacent to White (0)
    d. Green (3) if not adjacent to White (0).
"""

import numpy as np

def get_all_adjacent(grid, i, j):
    rows, cols = len(grid), len(grid[0])
    adjacent_cells = []
    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(cols, j + 2)):
            if (x, y) != (i, j):
                adjacent_cells.append((x, y, grid[x][y]))
    return adjacent_cells


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

                for x, y, val in get_all_adjacent(input_grid, i, j):
                    if val == 0:
                        if x == i:
                            is_horizontally_adjacent_to_0 = True
                        elif y == j:
                            is_vertically_adjacent_to_0 = True
                        else:
                            is_diagonally_adjacent_to_0 = True

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