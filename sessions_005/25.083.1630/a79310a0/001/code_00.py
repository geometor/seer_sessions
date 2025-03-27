"""
The program identifies contiguous blocks of azure (8) pixels in the input grid,
creates corresponding blocks of the same shape using red (2) pixels, and
positions these red blocks centered vertically and horizontally.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous blocks of a specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def find_center(obj):
    """
    Finds vertical and horizontal center based on original object shape y, x
    """
    min_row = min(point[0] for point in obj)
    max_row = max(point[0] for point in obj)
    min_col = min(point[1] for point in obj)
    max_col = max(point[1] for point in obj)

    center_row = min_row
    center_col = min_col

    return center_row, center_col

def transform(input_grid):
    # Initialize output_grid with zeros (white)
    output_grid = np.zeros_like(input_grid)

    # Find azure objects
    azure_objects = find_objects(input_grid, 8)
    
    # Create and position red objects
    for obj in azure_objects:
        # Find object center
        center_row, center_col = find_center(obj)

        # Create red object and place
        for row, col in obj:
            output_grid[row, col] = 0 #remove original
            output_grid[center_row, center_col] = 2


    return output_grid