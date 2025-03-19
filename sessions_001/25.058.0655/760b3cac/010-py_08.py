"""
The azure (8) object expands into adjacent empty (white, 0) cells to the right and down.
The expansion stops when the azure object encounters either a yellow (4) object or the edge of the grid. Yellow objects do not move.
"""

import numpy as np

def find_object(grid, color):
    """
    Finds the coordinates of all pixels of a specific color within the grid.
    """
    coords = np.argwhere(grid == color)
    return coords

def expand_azure(grid, azure_coords, yellow_coords):
    """
    Expands the azure object to the right and down, constrained by yellow objects and grid boundaries.
    """
    new_grid = np.copy(grid)
    # Convert yellow_coords to a set for efficient checking
    yellow_coords_set = set(map(tuple, yellow_coords))

    for r, c in azure_coords:
        # Expand right
        if c + 1 < grid.shape[1] and (r, c + 1) not in yellow_coords_set and grid[r, c+1] == 0:
            new_grid[r, c + 1] = 8
        # Expand down
        if r + 1 < grid.shape[0] and (r + 1, c) not in yellow_coords_set and grid[r+1, c] == 0:
            new_grid[r + 1, c] = 8
    return new_grid
    

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure shape (color 8).
    azure_coords = find_object(input_grid, 8)

    # Find the yellow shape (color 4).
    yellow_coords = find_object(input_grid, 4)

    # Expand the azure shape based on constraints
    output_grid = expand_azure(output_grid, azure_coords, yellow_coords)

    return output_grid