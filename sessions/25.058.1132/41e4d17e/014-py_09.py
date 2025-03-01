"""
1.  Identify all contiguous blue objects within the grid.
2.  For each enclosed area completely surrounded by a blue object, change every pixel within the area to magenta. It does not matter what color the enclosed pixels are, they all become magenta.
"""

import numpy as np

def get_objects(grid, color):
    """Find contiguous regions of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_neighbors(grid, r, c):
    """Get the coordinates of neighboring pixels."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                neighbors.append((nr, nc))
    return neighbors

def is_enclosed(grid, start_r, start_c, blue_pixels):
    """Checks if a region is completely enclosed by blue pixels."""
    color = grid[start_r, start_c]
    if color == 1:  # if it starts on blue, it's not enclosed
        return False

    visited = np.zeros_like(grid, dtype=bool)
    queue = [(start_r, start_c)]
    visited[start_r, start_c] = True
    enclosed = True

    while queue:
        r, c = queue.pop(0)

        for nr, nc in get_neighbors(grid, r, c):
            if not (0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]):  # If out of bounds
                enclosed = False
                continue
            if (nr, nc) in blue_pixels:  # It is blue
                continue
            if not visited[nr, nc]:
                if grid[nr,nc] != color:
                    #we've hit a boundary, it's not fully enclosed
                    enclosed = False
                visited[nr, nc] = True
                queue.append((nr, nc))
    return enclosed


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # get blue pixels
    blue_objects = get_objects(input_grid, 1)
    blue_pixels = set()
    for obj in blue_objects:
        blue_pixels.update(obj)
    
    # check for enclosed spaces and change to magenta
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if (r,c) not in blue_pixels:
          if is_enclosed(input_grid, r, c, blue_pixels):
              output_grid[r,c] = 6

    return output_grid