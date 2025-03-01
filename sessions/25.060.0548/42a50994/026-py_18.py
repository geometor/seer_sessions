"""
Transforms an input grid by preserving objects (contiguous blocks of non-white pixels) that have at least 3 pixels,
and removing objects with fewer than 3 pixels.
"""

import numpy as np

def find_objects(grid):
    """Finds all contiguous objects in a grid."""
    objects = {}
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def dfs(row, col, color, obj_id):
        """Depth-first search to find contiguous pixels of the same color."""
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        objects[obj_id]['pixels'].append((row, col))
        objects[obj_id]['count'] += 1

        # Explore adjacent cells (including diagonals)
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i != row or j != col:
                    dfs(i, j, color, obj_id)

    obj_id = 0
    for row in range(rows):
        for col in range(cols):
            color = grid[row, col]
            if color != 0 and not visited[row, col]:
                objects[obj_id] = {'color': color, 'pixels': [], 'count': 0}
                dfs(row, col, color, obj_id)
                obj_id += 1
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on object size.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Find all objects in the input grid.
    objects = find_objects(input_grid)

    # Iterate through the objects and remove those with fewer than 3 pixels.
    for obj_data in objects.values():
        if obj_data['count'] < 3:
            for row, col in obj_data['pixels']:
                output_grid[row, col] = 0  # Set pixel to white

    return output_grid