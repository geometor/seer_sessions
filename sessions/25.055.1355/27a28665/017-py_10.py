"""
Examine the input grid. If all pixels in the input grid have the same color, the output is a 1x1 grid with the color maroon (9). If the input grid has a 3x3 block of a single color and the rest of the grid is white (0), output green (3).
"""

import numpy as np

def is_uniform(grid):
    """Checks if the grid is uniform (all pixels have the same color)."""
    first_color = grid[0, 0]
    return np.all(grid == first_color)

def find_3x3_block(grid):
    """Checks if there's a 3x3 block of the same non-white color."""
    rows, cols = grid.shape
    for i in range(rows - 2):
        for j in range(cols - 2):
            subgrid = grid[i:i+3, j:j+3]
            if is_uniform(subgrid) and subgrid[0,0] != 0:
                return True
    return False
    
def check_mostly_white(grid, block_row, block_col):
    """Checks if rest of grid is white, assuming existence of 3x3."""
    rows, cols = grid.shape
    temp_grid = np.copy(grid)
    temp_grid[block_row:block_row+3, block_col:block_col+3] = 0
    if (np.all(temp_grid == 0)):
        return True
    return False
    
def find_3x3_block_and_white(grid):
    """Finds the 3x3 and checks remaining grid"""
    rows, cols = grid.shape
    for i in range(rows - 2):
        for j in range(cols - 2):
            subgrid = grid[i:i+3, j:j+3]
            if is_uniform(subgrid) and subgrid[0,0] != 0:
                if (check_mostly_white(grid, i, j)):
                    return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    input_grid = np.array(input_grid)

    # If the grid is uniform, output maroon (9).
    if is_uniform(input_grid):
        return np.array([[9]])

    # If there's a 3x3 block of a single non-white color, and the rest
    # is white, output green (3).
    if find_3x3_block_and_white(input_grid):
        return np.array([[3]])

    # Otherwise, no transformation rule applies (this shouldn't happen
    # based on current observations, but is included for completeness).
    return None