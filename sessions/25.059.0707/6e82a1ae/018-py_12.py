"""
The transformation identifies each disconnected gray object in the input grid and replaces all pixels of that object with a new color. Each object receives a unique color (blue, green, or red) in a cyclical manner. The background (white pixels) and any pre-existing non-gray colors remain unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds all distinct connected components of a given color in the grid.
    Returns a list of sets, where each set contains the coordinates of a connected component.
    """
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.add((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = set()
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by replacing each connected gray object with a unique color.
    """
    output_grid = np.copy(input_grid)
    gray_objects = find_objects(input_grid, 5)  # Find all gray objects

    # Define a color mapping for the objects - cyclical
    color_map = {
        0: 1,  # First object: blue
        1: 3,  # Second object: green
        2: 2,  # Third object: red
    }

    # Replace gray pixels with the corresponding color for each object
    for i, obj in enumerate(gray_objects):
        color_index = i % len(color_map)  # cycle through the colors: blue, green, red
        for r, c in obj:
            output_grid[r, c] = color_map[color_index]

    return output_grid