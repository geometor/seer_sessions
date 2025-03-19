"""
Identifies contiguous blocks of azure (8) pixels in a grid.
For each object, change the color of azure pixels that touch the edge of
the grid to blue (1)
"""

import numpy as np

def find_objects(grid, color):
    # Find all pixels of the target color.
    pixels = np.argwhere(grid == color)
    
    objects = []
    visited = set()

    # Breadth first search
    def bfs(r, c):
        obj = []
        queue = [(r, c)]
        visited.add((r, c))

        while queue:
            row, col = queue.pop(0)
            obj.append((row, col))

            # Check adjacent cells (up, down, left, right)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and (nr, nc) not in visited and grid[nr, nc] == color:
                    queue.append((nr, nc))
                    visited.add((nr, nc))
        return obj
    
    for r, c in pixels:
        if (r,c) not in visited:
           objects.append(bfs(r,c))

    return objects

def is_edge_pixel(grid, row, col):
    """Checks if a pixel is on the edge of the grid."""
    return row == 0 or row == grid.shape[0] - 1 or col == 0 or col == grid.shape[1] - 1

def transform(input_grid):
    """
    Transforms the input grid according to the rule: Change the color of
    single azure pixels touching edge within each azure object from azure (8)
    to blue (1).
    """
    output_grid = np.copy(input_grid)
    azure_objects = find_objects(input_grid, 8)

    for obj in azure_objects:
        for row, col in obj:
            # Check if any of the pixels that are single azure
            # and touch the edge needs color change
            if is_edge_pixel(input_grid, row, col):
                output_grid[row, col] = 1

    return output_grid