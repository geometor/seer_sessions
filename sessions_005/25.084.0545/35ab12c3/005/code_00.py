"""
1. Identify Objects: Find all distinct objects in the input grid. An object is a
   group of connected pixels of the same color (excluding black/0, which is
   considered background).
2. Iterate and Expand: Iterate through each identified object.
3. Expansion process:
    *  The non-zero colors expand into neighboring areas, including black/0
       background.
    * The objects appear to expand one layer at a time, respecting a precedence
      or rule when colors meet. This interaction rule between color is the
      current missing link. It's NOT simply "overwrite".
    * The final expansion appear to have horizontal and vertical lines - not
      diagonal.
    * Look for specific pairwise interaction rules.
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

def expand_object_one_layer(grid, pixels, color):
    """
    Expands an object by one layer, considering neighbors. This is a modified
    version to *only* expand one layer at a time, which will help in
    controlling the expansion process and implementing interaction rules.

    Args:
        grid: The current state of the grid.
        pixels: The current pixels of the object.
        color: The color of the object being expanded.

    Returns:
        A set of new pixel coordinates that represent the one-layer expansion.
    """
    expanded_pixels = set()
    for row, col in pixels:
        neighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]
        for r, c in neighbors:
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                expanded_pixels.add((r, c))  # Add all neighbors, we'll filter later
    return expanded_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()

    # 1. Find objects in the input grid.
    input_objects = find_objects(input_grid)

    # 2. Iterate through objects and expand one layer at a time.
    #    The interaction rules are still unknown, but we'll expand one layer
    #    at a time and attempt to determine rules as we execute this and
    #    analyze.
    all_colors = sorted(input_objects.keys())  # Process in color order
    for color in all_colors:
      pixels = input_objects[color]
      expanded_pixels = expand_object_one_layer(output_grid, pixels, color)

      # Apply expansion, but only to cells that were originally 0
      for r, c in expanded_pixels:
            if input_grid[r,c] == 0:
              output_grid[r,c] = color


    return output_grid