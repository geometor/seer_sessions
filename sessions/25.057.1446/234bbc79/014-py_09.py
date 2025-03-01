"""
The transformation rule involves identifying specific colored objects (gray and azure) in the input grid, swapping their colors, and shifting all other objects one position to the right.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) tuples.
    """
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    - Gray (5) objects become Azure (8).
    - Azure (8) objects adjacent to the right of gray objects become magenta (6).
    - Other objects are shifted one position to the right in the output.
    """
    output_grid = np.zeros_like(input_grid)
    objects = find_objects(input_grid)

    for obj in objects:
        first_pixel_r, first_pixel_c = obj[0]
        color = input_grid[first_pixel_r, first_pixel_c]

        if color == 5:  # Gray
            for r, c in obj:
                output_grid[r, c] = 8  # Change to Azure
        elif color == 8:  # Azure
             #check if there's gray to the left
            is_next_to_gray = False
            for r, c in obj:
                if (r,c-1) in [(r_gray,c_gray) for gray_obj in objects for r_gray, c_gray in gray_obj if input_grid[r_gray,c_gray]==5]:
                    is_next_to_gray = True
                    break;
            if is_next_to_gray:
                for r, c in obj:
                    output_grid[r, c] = 6 #Change to magenta
            else: # other objects move 1 to right
                 for r, c in obj:
                    if c + 1 < output_grid.shape[1]:
                        output_grid[r,c+1] = color

        else: # other objects move 1 to right
            for r, c in obj:
                if c + 1 < output_grid.shape[1]:
                    output_grid[r, c + 1] = color

    return output_grid