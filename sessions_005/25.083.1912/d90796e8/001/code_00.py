"""
If a red (2) and green (3) pixel are touching (orthogonally or diagonally), the green or red pixel is changed to azure (8). All other colors are unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Gets the neighbors of cell.
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row = row + i
            neighbor_col = col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the rule: If a red (2) and green (3) pixel
    are touching (orthogonally or diagonally), change the green or red cell to
    azure (8).
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            # skip if is not 2 or 3
            if input_grid[row,col] not in [2,3]:
                continue

            neighbors = get_neighbors(input_grid, row, col)
            
            for neighbor_row, neighbor_col in neighbors:              
                # if current cell is 3, change it if the neighbor is 2
                if input_grid[row,col] == 3 and input_grid[neighbor_row, neighbor_col] == 2:
                    output_grid[row, col] = 8
                #if current cell is 2, change it if the neighbor is 3
                elif input_grid[row, col] == 2 and input_grid[neighbor_row, neighbor_col] == 3:
                    output_grid[row,col] = 8
    return output_grid