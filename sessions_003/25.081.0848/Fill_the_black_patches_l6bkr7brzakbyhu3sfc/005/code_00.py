"""
Fills zero-valued pixels in a grid with the color of the surrounding connected region.
"""

import numpy as np

def get_all_neighbors(grid, row, col):
    """Gets the colors of all 8 neighbors (including diagonals)."""
    rows, cols = grid.shape
    neighbors = {}
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the cell itself
                neighbors[(i,j)] = grid[i, j]
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 0:
                # Get colors of all 8 neighbors.
                neighbor_colors = get_all_neighbors(input_grid, row, col)
                neighbor_values = list(neighbor_colors.values())
                #find non zero neighbors
                non_zero_neighbors = [val for val in neighbor_values if val != 0]
                # Count the occurrences of each non-zero color
                
                if len(set(non_zero_neighbors)) == 1:
                    #fill value if there is only 1
                    output_grid[row,col] = non_zero_neighbors[0]

    return output_grid