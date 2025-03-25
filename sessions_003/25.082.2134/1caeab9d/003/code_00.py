"""
The transformation rule involves identifying contiguous blocks of non-zero (non-white) colored pixels in the input grid and consolidating them horizontally. 
Colored blocks of the same color that are not adjacent are made to be adjacent, effectively consolidating them.
The order and relative layout of distinct colored blocks are maintained, and all objects are moved to a single, vertically-centered row.
"""

import numpy as np

def get_objects(grid):
    """
    Finds all contiguous blocks of non-zero pixels in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append((grid[row, col], obj))  # Store color and object pixels
    return objects

def transform(input_grid):
    # Initialize output_grid as a zero-filled grid of the same size as the input
    output_grid = np.zeros_like(input_grid)

    # Get objects from the input grid
    objects = get_objects(input_grid)

    # Sort objects by their original appearance (top-to-bottom, left-to-right)
    objects_sorted = sorted(objects, key=lambda x: (min(p[0] for p in x[1]), min(p[1] for p in x[1])))

    # Determine the center row of the input grid
    center_row = input_grid.shape[0] // 2

    # Consolidate and place objects
    next_col = 0
    for color, obj in objects_sorted:
        # Place each object on the center row, shifting it to the next available column
        for row, col in obj:
            output_grid[center_row, next_col] = color
            next_col += 1

    return output_grid