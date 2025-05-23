"""
The program expands some objects in the input grid outwards, but the expansion rule
isn't a simple uniform one. It appears to involve a selective flood-fill like
behavior where expansion is influenced by the presence and type of neighboring
pixels, both background (white/0) and colored. It's flood fill into existing
non-zero colors.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in a grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A dictionary where keys are colors and values are lists of (row, col)
        tuples representing the object's pixels.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return []

        visited.add((row, col))
        pixels = [(row, col)]
        pixels.extend(dfs(row + 1, col, color))
        pixels.extend(dfs(row - 1, col, color))
        pixels.extend(dfs(row, col + 1, color))
        pixels.extend(dfs(row, col - 1, color))
        return pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if (row, col) not in visited and color != 0:
                if color not in objects:
                    objects[color] = []
                objects[color].extend(dfs(row, col, color))

    return objects

def expand_object(grid, pixels, color):
    """
    Expands an object outwards in all directions, also into non-zero
    colors.

    Args:
       grid: grid to perform expansion in
       pixels: object pixel coordinates
       color: object color
    """
    expanded_pixels = set(pixels)
    queue = list(pixels)

    while queue:
        row, col = queue.pop(0)

        neighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]

        for r, c in neighbors:
            if (
                0 <= r < grid.shape[0]
                and 0 <= c < grid.shape[1]
                and (grid[r,c] == 0 or grid[r,c] != color)
                and (r, c) not in expanded_pixels
            ):
                expanded_pixels.add((r, c))
                queue.append((r, c))
    return list(expanded_pixels)



def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # change output pixels
    # 1. Find objects in the input grid.
    input_objects = find_objects(input_grid)

    # 2. Iterate through objects and expand, overwriting existing colors.
    for color, pixels in input_objects.items():
        expanded_pixels = expand_object(input_grid, pixels, color)
        for r, c in expanded_pixels:
            output_grid[r,c] = color

    return output_grid