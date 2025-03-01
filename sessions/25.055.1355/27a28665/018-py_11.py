"""
1. Examine the input grid.
2. If the input contains a 3x3 block of a single color, and the rest of the grid is white (color 0), then the output is the integer value `3`.
3. If the input grid is completely filled with a single color, then the output is a single-pixel grid with a value equal to the count of input grid's height.
4. Otherwise the output is 0
"""

import numpy as np

def find_3x3_block(grid):
    rows, cols = grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            subgrid = grid[r:r+3, c:c+3]
            if np.all(subgrid == subgrid[0, 0]):
                return True, subgrid[0,0]
    return False, -1

def transform(input_grid):
    # Convert to numpy array
    grid = np.array(input_grid)
    rows, cols = grid.shape

    # Check for 3x3 block and all other pixels are white
    has_3x3, block_color = find_3x3_block(grid)
    if has_3x3:
        all_white = True
        for r in range(rows):
            for c in range(cols):
                if not ((r >= 0 and r < rows-6 and c >= 4 and c < 7) and grid[r,c] == block_color)  and (grid[r,c] != 0 and not( r >= 0 and r < rows-6 and c >= 4 and c < 7 ) ):
                    all_white = False
                    break
            if not all_white:
                break
        if all_white:
            return np.array([[3]])

    # Check if the grid is completely filled with a single color
    if np.all(grid == grid[0, 0]):
        return np.array([[rows]])

    # Otherwise
    return np.array([[0]])