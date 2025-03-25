"""
The transformation mirrors/inverts/transposes the position of the colored object in the input grid, 
maintaining the original grid size.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects (same color pixels) in a grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row,col] != 5 and grid[row,col] != 0:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by inverting the objects.

    """
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.full(input_grid.shape, 0)

    # Find objects
    objects = find_objects(input_grid)

    # Invert/transpose/mirror object positions
    for obj in objects:
        for row, col in obj:
            # output_grid[input_grid.shape[0] - 1 - row, input_grid.shape[1] - 1- col] = input_grid[row, col] #Invert
            # output_grid[col, row] = input_grid[row, col] # Transpose
             output_grid[input_grid.shape[0] - 1 - row, col] = input_grid[row, col]  # Mirror/Invert
    return output_grid.tolist()