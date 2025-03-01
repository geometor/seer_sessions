"""
The transformation rule is to double the width of the input grid while maintaining the same number of rows. Each object within the input grid, defined as a contiguous block of pixels of the same color, is duplicated horizontally. The white background (color 0) is also extended to fill the remaining space in the doubled-width output grid. The row and col position is preserved.
"""

import numpy as np

def get_objects(grid):
    """
    Identify contiguous objects (blocks of same color) in a grid.
    """
    objects = []
    visited = set()

    def dfs(row, col, color, obj):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                obj = []
                dfs(row, col, grid[row, col], obj)
                if obj:
                    objects.append(obj)
    return objects

def transform(input_grid):
    # Initialize the output grid with double the width and same height, filled with white (0)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols * 2), dtype=int)

    # Get the objects in the input grid
    input_objects = get_objects(input_grid)

    # Duplicate each object horizontally
    for obj in input_objects:
        for row, col in obj:
            # Original object position
            output_grid[row, col] = input_grid[row, col]
            # Duplicated object position
            output_grid[row, col + cols] = input_grid[row, col]

    return output_grid