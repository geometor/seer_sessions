"""
The transformation rule is to identify the largest object in the input grid and create an output grid of the same dimensions filled with the color of that object. If there are multiple objects of the same largest size, the color of the object that comes first in the top-to-bottom, left-to-right scan is used.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all objects in the grid and returns a list of (color, size, coordinates) tuples.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, color, coordinates):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != color:
            return
        visited.add((r, c))
        coordinates.append((r, c))
        dfs(r + 1, c, color, coordinates)
        dfs(r - 1, c, color, coordinates)
        dfs(r, c + 1, color, coordinates)
        dfs(r, c - 1, color, coordinates)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r][c]
                coordinates = []
                dfs(r, c, color, coordinates)
                objects.append((color, len(coordinates), coordinates))
    return objects

def transform(input_grid):
    """
    Transforms the input grid by filling the output grid with the color of the largest object.
    """
    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # Find the largest object(s)
    max_size = 0
    largest_objects = []
    for color, size, _ in objects:
        if size > max_size:
            max_size = size
            largest_objects = [(color, size)]
        elif size == max_size:
            largest_objects.append((color, size))
            
    # Determine dominant color (color of the first largest object encountered)
    dominant_color = largest_objects[0][0]

    # Create an output grid of the same dimensions, filled with the dominant color
    output_grid = np.full((len(input_grid), len(input_grid[0])), dominant_color)

    return output_grid.tolist()