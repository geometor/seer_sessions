"""
The transformation rule involves counting the number of distinct azure (8) colored objects in the input grid and outputting that count.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous objects of a specified color in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color and not visited[i, j]:
                dfs(i, j)
                objects.append(1)  # Append 1 to signify finding one distinct object
    return objects
def transform(input_grid):
    """
    Counts the number of distinct azure (8) objects and returns the count.
    """
    # Find azure objects
    azure_objects = find_objects(input_grid, 8)
    
    # Count the number of distinct objects found.
    object_count = sum(azure_objects)
    
    # Return the count as a 1x1 grid.
    
    output_grid = np.array([[object_count]])

    return output_grid