"""
Iterate through each pixel of the input grid. For each pixel:

1.  Check if the current pixel is green (3).
2.  If it is green, check its adjacent pixels (both orthogonal and diagonal neighbors).
3.  If any of the adjacent pixels is red (2), change the current green pixel to azure (8) and the red pixel to black (0).
4. If the current pixel is *not* green, it is unchanged.
5. If the current pixel is green, but *no* adjacent cells are red, it is unchanged.
6. Repeat for all grid positions.
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
    Transforms the input grid according to the rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is green (3)
            if input_grid[row, col] == 3:
                neighbors = get_neighbors(input_grid, row, col)
                for neighbor_row, neighbor_col in neighbors:
                    # If a neighbor is red (2), change both pixels
                    if input_grid[neighbor_row, neighbor_col] == 2:
                        output_grid[row, col] = 8  # Change green to azure
                        output_grid[neighbor_row, neighbor_col] = 0  # Change red to black
                        # critically, we do NOT break, in case multiple red
                        # neighbors exist

    return output_grid