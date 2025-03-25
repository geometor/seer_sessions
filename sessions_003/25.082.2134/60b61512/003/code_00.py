"""
The transformation rule identifies yellow (4) clusters and their adjacent pixels. 
Empty (0) pixels adjacent to yellow pixels are replaced with orange (7). 
Yellow pixels adjacent to the newly changed orange pixels are *not* changed.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    helper: get all neighbors (including diagonals) of cell
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # store newly changed orange pixels
    orange_pixels = []

    # change white (0) pixels next to yellow to orange (7)
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 0:
                neighbors = get_neighbors(input_grid, row, col)
                for n_row, n_col in neighbors:
                    if input_grid[n_row, n_col] == 4:
                        output_grid[row, col] = 7
                        orange_pixels.append((row,col)) # save for later
                        break # only need one
    

    return output_grid