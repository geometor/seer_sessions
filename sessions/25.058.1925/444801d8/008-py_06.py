"""
Fills the area enclosed by a blue shape, starting from a red seed pixel, with red.
Correctly handles disjoint blue shapes by identifying the one containing the red seed.
Uses a ray-casting algorithm to accurately determine which pixels are inside the blue shape.
"""

import numpy as np

def find_object(grid, color):
    """Finds coordinates of all pixels of the specified color."""
    coords = np.argwhere(grid == color)
    return coords

def find_enclosing_shape(grid, seed_row, seed_col, shape_color):
    """
    Finds the shape of a specific color that encloses the seed point.
    Uses a flood-fill-like approach to identify connected components.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    shape_coords = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != shape_color:
            return

        visited[r, c] = True
        shape_coords.append((r, c))

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(seed_row, seed_col)
    return shape_coords

def is_within_shape(row, col, shape_coords):
    """
    Checks if a given (row, col) is within the bounds of a shape defined by
    shape_coords using the ray-casting algorithm.
    """
    if (row, col) in shape_coords:
        return False

    intersections = 0
    x, y = col, row  # For ray-casting, treat row as y and col as x

    for i in range(len(shape_coords)):
        x1, y1 = shape_coords[i][1], shape_coords[i][0]
        x2, y2 = shape_coords[(i + 1) % len(shape_coords)][1], shape_coords[(i + 1) % len(shape_coords)][0]

        if (y1 <= y < y2 or y2 <= y < y1) and \
           x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            intersections += 1

    return intersections % 2 == 1



def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the red pixel (seed).
    red_coords = find_object(input_grid, 2)
    if len(red_coords) == 0:
        return output_grid  # If no red pixel, return the original grid

    red_row, red_col = red_coords[0]

    # Find the blue shape containing the red seed.
    enclosing_blue_shape_coords = find_enclosing_shape(input_grid, red_row, red_col, 1)

    #if there is no blue shape containing the red seed, return grid
    if not enclosing_blue_shape_coords:
        return output_grid
   
    #Fill using ray-casting
    rows, cols = output_grid.shape
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0 and is_within_shape(r, c, enclosing_blue_shape_coords):
                output_grid[r,c] = 2

    output_grid[red_row, red_col] = 2 #ensure that original red pixel is red

    return output_grid