"""
Transforms the input grid by replacing colors 0, 7, 9 with output colors.
The output grid is the same shape as the input
The bounding box for all objects are identified in input. 
The bounding box is used to transform the output grid to the identified color.
"""

import numpy as np

def get_objects(grid):
    """Find contiguous blocks of the same color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, obj):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append((grid[row, col], obj))  # Store color and object pixels
    return objects

def get_bounding_box(obj):
    """Calculates the bounding box for set of pixels

    Args:
        obj (list): list of tuples, with the x and y coordinates

    Returns:
        tuple: coordinates of bounding box (min_row, min_col, max_row, max_col)
    """
    min_row = min(p[0] for p in obj)
    min_col = min(p[1] for p in obj)
    max_row = max(p[0] for p in obj)
    max_col = max(p[1] for p in obj)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Transforms the input grid based on color priority and simplification to rectangles.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(input_grid).copy()

    # get objects
    objects = get_objects(input_grid)
   
    # remove colors 0, 7, and 9
    objects = [(c, o) for c, o in objects if c not in [0,7,9]]
    
    # draw bounding box for remaining objects
    for color, obj in objects:
      min_row, min_col, max_row, max_col = get_bounding_box(obj)
      output_grid[min_row:max_row+1, min_col:max_col+1] = color
    
    return output_grid.tolist()