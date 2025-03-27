"""
Blue pixels adjacent to white pixels are changed to orange to create a one-pixel thick outline adjacent to white shapes.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the 8-connected neighbors of a pixel in the grid.
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row, neighbor_col = row + i, col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def count_orange_neighbors(grid, neighbors):
    """Counts the number of orange neighbors."""
    count = 0
    for r, c in neighbors:
        if grid[r, c] == 7:
            count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 1:
                neighbors = get_neighbors(output_grid, row, col)
                is_adjacent_to_white = any(output_grid[r, c] == 0 for r, c in neighbors)
                
                if is_adjacent_to_white:
                    # Check if it's part of an existing outline (already has orange neighbors)
                    orange_neighbors = count_orange_neighbors(output_grid, neighbors)

                    if orange_neighbors == 0:
                        output_grid[row, col] = 7
                    elif orange_neighbors < 3:
                        # check that neighbors do not include orange and more than 2 blues
                        will_thicken=False
                        for n_row, n_col in neighbors:
                            if output_grid[n_row,n_col] == 7:
                                nn = get_neighbors(output_grid, n_row, n_col)
                                if count_orange_neighbors(output_grid, nn) > 1 :
                                    will_thicken = True
                                    break
                        if not will_thicken: output_grid[row,col] = 7

    return output_grid