"""
1. **Grid Expansion:** Double the dimensions of the input grid to create the output grid.  Each cell (i, j) in the input grid will correspond to a 2x2 block of cells in the output grid, starting at position (2i, 2j).

2. **2x2 Block Generation:** The values within each 2x2 block of the output grid are determined by the following logic:

    - Inspect the value `v` of cell `input_grid[i][j]`
    - Get the adjacent horizontal and vertical cells: `left` is `input_grid[i][j-1]`,
     `right` is `input_grid[i][j+1]`, `above` is `input_grid[i-1][j]`, and `below`
     is `input_grid[i+1][j]`
    - If a neighbor does not exist (edge or corner) treat it as zero.
    - `output_grid[2*i][2*j]     = v if v != 0 else (left if left != 0 else (above if above !=0 else 0))`
    - `output_grid[2*i][2*j + 1] = v if v != 0 else (right if right != 0 else (above if above != 0 else 0))`
    - `output_grid[2*i + 1][2*j] = v if v!= 0 else (left if left != 0 else (below if below != 0 else 0))`
    - `output_grid[2*i + 1][2*j + 1] = v if v!= 0 else (right if right != 0 else (below if below != 0 else 0))`

    In summary - the top left pixel of the 2x2 output block will be the
    original input pixel if non-zero. If the input pixel is zero, the top, left,
    right and bottom are used to fill in the missing values of the 2x2 output
    block.
"""

import numpy as np

def get_neighbor(grid, i, j, direction):
    """Gets the value of a neighbor in a specified direction, handling edges."""
    rows, cols = grid.shape
    if direction == 'left':
        return grid[i, j - 1] if j > 0 else 0
    elif direction == 'right':
        return grid[i, j + 1] if j < cols - 1 else 0
    elif direction == 'above':
        return grid[i - 1, j] if i > 0 else 0
    elif direction == 'below':
        return grid[i + 1, j] if i < rows - 1 else 0
    else:
        return 0


def transform(input_grid):
    # Initialize output_grid with zeros, double the size of input_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Iterate through each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            v = input_grid[i, j]
            left = get_neighbor(input_grid, i, j, 'left')
            right = get_neighbor(input_grid, i, j, 'right')
            above = get_neighbor(input_grid, i, j, 'above')
            below = get_neighbor(input_grid, i, j, 'below')

            output_grid[2 * i, 2 * j] = v if v != 0 else (left if left != 0 else (above if above != 0 else 0))
            output_grid[2 * i, 2 * j + 1] = v if v != 0 else (right if right != 0 else (above if above != 0 else 0))
            output_grid[2 * i + 1, 2 * j] = v if v != 0 else (left if left != 0 else (below if below != 0 else 0))
            output_grid[2 * i + 1, 2 * j + 1] = v if v != 0 else (right if right != 0 else (below if below != 0 else 0))

    return output_grid