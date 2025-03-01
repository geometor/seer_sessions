"""
Identifies all contiguous regions (objects) of the same color within the input grid and reconstructs them in the output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    Returns a list of objects, where each object is a set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object, color):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.add((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, current_object, color)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and (row, col) not in visited:
                current_object = set()
                dfs(row, col, current_object, grid[row, col])
                objects.append((current_object, grid[row,col]))  # Store the object and its color
    return objects

def transform(input_grid):
    """
    Transforms the input grid by copying identified objects.
    """
    grid = np.array(input_grid)  # Convert to NumPy array
    objects = find_objects(grid)
    output_grid = np.zeros_like(grid)

    # Copy identified objects to output_grid
    for obj, color in objects:
        for row, col in obj:
            output_grid[row, col] = color

    return output_grid.tolist()