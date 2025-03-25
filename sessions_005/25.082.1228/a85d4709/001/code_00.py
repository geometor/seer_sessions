"""
Transforms an input grid to an output grid based on a color mapping rule. 

The rule is:
1. White (0) in the input becomes Green (3) in the output.
2. Gray (5) in the input becomes:
    a. Red (2) if vertically adjacent to White (0).
    b. Yellow (4) if horizontally adjacent to White (0).
    c. Green (3) if adjacent to Gray(5)
"""

import numpy as np

def get_adjacent(grid, i, j):
    rows, cols = len(grid), len(grid[0])
    adjacent_cells = []
    if i > 0:
        adjacent_cells.append((i - 1, j, grid[i-1][j])) # Up
    if i < rows - 1:
        adjacent_cells.append((i + 1, j, grid[i+1][j])) # Down
    if j > 0:
        adjacent_cells.append((i, j - 1, grid[i][j-1])) # Left
    if j < cols - 1:
        adjacent_cells.append((i, j + 1, grid[i][j+1])) # Right

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
                is_adjacent_to_5 = False

                for x,y, val in get_adjacent(input_grid, i, j):
                  if val == 0:
                    if x == i:
                        is_horizontally_adjacent_to_0 = True
                    if y == j:
                        is_vertically_adjacent_to_0 = True
                  if val == 5:
                    is_adjacent_to_5 = True


                if is_vertically_adjacent_to_0:
                    output_grid[i][j] = 2
                elif is_horizontally_adjacent_to_0:
                    output_grid[i][j] = 4
                elif is_adjacent_to_5:
                    output_grid[i][j] = 3


    return output_grid