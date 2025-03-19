"""
1. Identify Red Objects: Locate all contiguous regions of red (2) pixels.
2. Identify Adjacent Blue Pixels: For each red object, find all blue (1) pixels that are directly adjacent (sharing a side) to any part of the red object.
3. Transform Adjacent Blue Pixels: If a blue pixel is adjacent to any red pixel, change the blue pixel to yellow (4). It does not need to be fully enclosed.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of neighboring pixel coordinates for a given cell (only orthogonal).
    """
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def find_objects(grid, color):
    """
    Finds contiguous regions (objects) of a specific color in the grid.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        for neighbor_row, neighbor_col in get_neighbors(grid, row, col):
            dfs(neighbor_row, neighbor_col, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the adjacency rule.
    """
    output_grid = np.copy(input_grid)
    red_objects = find_objects(input_grid, 2)

    # Create a set of all red pixel coordinates for efficient adjacency checking
    red_pixels = set()
    for obj in red_objects:
      red_pixels.update(obj)

    # Iterate through all cells, checking for blue pixels adjacent to red
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 1:  # If it's a blue pixel
                is_adjacent = False
                for neighbor_row, neighbor_col in get_neighbors(input_grid, row, col):
                    if (neighbor_row, neighbor_col) in red_pixels:
                        is_adjacent = True
                        break  # No need to check other neighbors
                if is_adjacent:
                    output_grid[row, col] = 4  # Change to yellow

    return output_grid