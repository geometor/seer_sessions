"""
The azure (8) object expands simultaneously in all directions (up, down, left, and right) into adjacent empty (white, 0) cells. The expansion stops when the expanding azure object encounters either a yellow (4) object or the edge of the grid. Yellow objects do not move. The expansion propagates such that all azure pixels expand to adjacent white cells at each step.
"""

import numpy as np

def find_object(grid, color):
    """
    Finds the coordinates of all pixels of a specific color within the grid.
    """
    coords = np.argwhere(grid == color)
    return coords

def expand_azure(grid, azure_coords, yellow_coords_set):
    """
    Expands the azure object one step in all directions, constrained by yellow objects and grid boundaries.
    Returns the new azure coordinates and a boolean indicating if any expansion occurred.
    """
    new_azure_coords = set()
    expansion_occurred = False

    for r, c in azure_coords:
        new_azure_coords.add((r, c))  # Keep existing azure pixels
        # Check adjacent cells
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check boundaries and if it's a white cell not blocked by yellow
            if (0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and
                (nr, nc) not in yellow_coords_set and grid[nr, nc] == 0):
                new_azure_coords.add((nr, nc))
                expansion_occurred = True

    return new_azure_coords, expansion_occurred


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the yellow shape (color 4).  Convert to a set for efficient checking.
    yellow_coords_set = set(map(tuple, find_object(input_grid, 4)))

    # Find initial azure coordinates
    azure_coords = set(map(tuple, find_object(input_grid, 8)))


    # Expand azure iteratively until no more expansion occurs
    expansion_possible = True
    while expansion_possible:
        azure_coords, expansion_possible = expand_azure(output_grid, azure_coords, yellow_coords_set)

        # Apply changes to the output_grid during the expansion.
        # Create a temporary grid each time to update based on current expansion step.
        temp_grid = np.copy(output_grid)
        for r, c in azure_coords:
            temp_grid[r,c] = 8
        output_grid = temp_grid

    return output_grid