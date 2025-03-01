# 7b6016b9 • 018 • refine_coder

---
```python
"""
1. Background Fill: Change all white (0) pixels to green (3).
2. Identify Yellow Objects: Identify all contiguous regions (objects) of yellow (4) pixels. Contiguous means orthogonally connected (up, down, left, right - not diagonal).
3. Preserve Yellow Objects: Copy all yellow (4) pixels from the input to the output.
4. Interior Fill: For *each* green (3) pixel in the output, determine if it lies *inside* any of the yellow objects. If it does, change it to red (2). A pixel is considered "inside" a yellow object if it is not part of the object and requires crossing the object to reach the edge of the grid.
5. Multiple Objects: This should now correctly process multiple, possibly irregular shaped objects of color 4.
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
    Uses a ray-casting approach, counting intersections with object boundaries.
    """
    if any((r, c) in obj for obj in objects):
        return False  # Cell is part of an object, so not inside

    all_object_pixels = set()
    for obj in objects:
        all_object_pixels.update(obj)

    intersections = 0
    # Cast a ray to the right.  Other directions could be added for robustness,
    # but for this task, a single direction seems sufficient based on tests.
    for c2 in range(c + 1, grid_shape[1]):
        if (r, c2) in all_object_pixels:
            # Check if we actually cross a boundary, and it is not a
            # grazing contact.  Look above and below to determine.
            is_above = (r - 1, c2) in all_object_pixels
            is_below = (r + 1, c2) in all_object_pixels
            if not (is_above and is_below):
                intersections += 1

    return intersections % 2 == 1  # Odd number of intersections means inside


def transform(input_grid):
    # Initialize output_grid with green (3) - filling the background
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
