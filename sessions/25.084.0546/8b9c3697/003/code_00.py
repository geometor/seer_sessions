"""
Find all red (2) objects and replace them with color white (0), while all other colors are maintained.
"""

import numpy as np

def get_neighbors(pos, grid_shape):
    """
    Returns the valid neighboring positions (including diagonals) for a given position.
    """
    row, col = pos
    neighbors = []
    for i in range(max(0, row - 1), min(grid_shape[0], row + 2)):
        for j in range(max(0, col - 1), min(grid_shape[1], col + 2)):
            if (i, j) != pos:
                neighbors.append((i, j))
    return neighbors

def find_object(grid, start_pos, color):
    """
    Finds a contiguous object of the given color starting from a given position.
    Uses a Depth-First Search (DFS) approach.
    """
    object_pixels = set()
    visited = set()
    stack = [start_pos]

    while stack:
        pos = stack.pop()
        if pos in visited:
            continue
        visited.add(pos)

        if grid[pos] == color:
            object_pixels.add(pos)
            neighbors = get_neighbors(pos, grid.shape)
            for neighbor in neighbors:
                stack.append(neighbor)

    return object_pixels

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    grid_shape = output_grid.shape
    visited = set()

    # Iterate through each pixel in the grid
    for row in range(grid_shape[0]):
        for col in range(grid_shape[1]):
            pos = (row, col)
            if pos not in visited:
                current_color = output_grid[pos]
                # Find the object containing the current pixel
                current_object = find_object(output_grid, pos, current_color)
                visited.update(current_object)

                # Check if the object's color is red (2)
                if current_color == 2:
                    # Replace all pixels in the red object with white (0)
                    for obj_pos in current_object:
                        output_grid[obj_pos] = 0

    return output_grid