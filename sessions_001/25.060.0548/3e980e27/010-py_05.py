"""
The transformation rule is to mirror the positions of all non-zero colored objects both horizontally and vertically across the center of the grid.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous clusters of non-zero pixels.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def mirror_position(pos, grid_shape):
    """
    Calculates the mirrored position of a coordinate across both axes.

    Args:
        pos: A tuple (row, col) representing the original position.
        grid_shape: A tuple (rows, cols) representing the grid dimensions.

    Returns:
        A tuple (mirrored_row, mirrored_col) representing the new position.
    """
    rows, cols = grid_shape
    mirrored_row = rows - 1 - pos[0]
    mirrored_col = cols - 1 - pos[1]
    return (mirrored_row, mirrored_col)

def transform(input_grid):
    """
    Transforms the input grid by mirroring objects horizontally and vertically.
    """
    input_grid = np.array(input_grid)  # Ensure numpy array for easier manipulation
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # Mirror each object and update the output grid
    for obj in objects:
        for r, c in obj:
            mirrored_r, mirrored_c = mirror_position((r, c), (rows, cols))
            output_grid[mirrored_r, mirrored_c] = input_grid[r, c]

    return output_grid.tolist()