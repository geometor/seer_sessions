# 7b6016b9 • 020 • refine_coder

---
```python
"""
1.  **Background Initialization:** Fill the entire output grid with green (color 3).

2.  **Object Identification:** Identify all contiguous regions (objects) of yellow (color 4) pixels in the input grid. Contiguous pixels are orthogonally connected (up, down, left, right).

3.  **Object Preservation:** Copy all yellow pixels from the input grid to their corresponding positions in the output grid.

4.  **Interior Filling:** For each green pixel in the *output* grid, determine if it lies *inside* any of the yellow objects. A green pixel is considered "inside" a yellow object if it's not part of the object itself and *any* attempt to draw a straight line (orthogonally or diagonally) from that pixel to any edge of the grid intersects with the yellow object an *odd* number of times. If a pixel is determined to be inside a yellow object, change its color to red (color 2).
The ray trace should count the intersection, and an odd number of intersections will indicate the position is inside the object.
"""

import numpy as np

def get_objects(grid, color):
    """
    Finds objects of a specific color in the grid.
    An "object" is a set of orthogonally connected pixels of the same color.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return

        visited[r, c] = True
        current_object.append((r, c))

        # Explore orthogonal neighbors (up, down, left, right)
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

def is_inside(r, c, objects, grid_shape):
    """
    Checks if a given cell (r, c) is "inside" any of the objects.
    Uses a ray-casting approach, counting intersections with object boundaries in all 8 directions.
    """
    if any((r, c) in obj for obj in objects):
        return False  # Cell is part of an object, so not inside

    all_object_pixels = set()
    for obj in objects:
        all_object_pixels.update(obj)

    intersections = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)] # all 8 directions

    for dr, dc in directions:
        current_r, current_c = r + dr, c + dc
        while 0 <= current_r < grid_shape[0] and 0 <= current_c < grid_shape[1]:
            if (current_r, current_c) in all_object_pixels:
                # Check boundary crossing (avoid grazing)
                is_above = (current_r - dr, current_c - dc) in all_object_pixels
                is_below = (current_r + dr, current_c+ dc) in all_object_pixels
                if not (is_above and is_below):
                    intersections += 1
            current_r += dr
            current_c += dc

    return intersections % 2 == 1

def transform(input_grid):
    # Initialize output_grid with green (3)
    output_grid = np.full_like(input_grid, 3)

    # Identify Yellow Objects
    yellow_objects = get_objects(input_grid, 4)

    # Preserve Yellow Objects: Copy yellow (4) pixels from input to output
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 4:
                output_grid[r, c] = 4

    # Interior Fill: Change green (3) pixels inside the yellow objects to red (2)
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r, c] == 3:
                if is_inside(r, c, yellow_objects, output_grid.shape):
                    output_grid[r, c] = 2

    return output_grid
```
