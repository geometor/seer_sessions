"""
Transforms an input grid containing mostly 0s (white) and a few 8s (azure) into an output grid with a significantly larger number of 8s. The 8s in the input act as "seeds" that expand outwards in a complex, somewhat irregular pattern, creating interlocking regions of azure.
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonal=True):
    """Gets the neighbors of a cell, optionally including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not include_diagonal and (abs(i) + abs(j) != 1):
                continue
            neighbor_row, neighbor_col = row + i, col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def expand_seed(grid, row, col, expanded_grid):
    """Expands a single seed pixel outwards."""
    rows, cols = grid.shape
    queue = [(row, col)]
    expanded_grid[row, col] = 8

    while queue:
        curr_row, curr_col = queue.pop(0)

        neighbors = get_neighbors(grid, curr_row, curr_col, include_diagonal=True)
        for neighbor_row, neighbor_col in neighbors:
            if expanded_grid[neighbor_row, neighbor_col] == 0:
                # Check for nearby 8s to maintain boundaries
                nearby_8s = 0
                neighbor_neighbors = get_neighbors(expanded_grid, neighbor_row, neighbor_col)
                for nn_row, nn_col in neighbor_neighbors:
                     if expanded_grid[nn_row, nn_col] == 8:
                            nearby_8s+=1


                if nearby_8s <= 3 :
                  expanded_grid[neighbor_row, neighbor_col] = 8
                  queue.append((neighbor_row, neighbor_col))


def transform(input_grid):
    """Transforms the input grid according to the expansion rules."""
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find seed pixels (value 8)
    seed_pixels = []
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 8:
                seed_pixels.append((row, col))

    #expand the grid multiple times
    for i in range(5):

        # Expand each seed pixel
        expanded_grid = np.copy(output_grid)
        for row, col in seed_pixels:
            expand_seed(output_grid, row, col, expanded_grid)

        output_grid = expanded_grid



    return output_grid