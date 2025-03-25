```python
"""
1.  **Object Identification:** Identify distinct objects within the grid. An object is a contiguous group of pixels of the same color. Contiguous means connected horizontally or vertically. Ignore objects of color 7.

2.  **Iterate:** For each identified object:

3.  **Red Object Transformation:**
    *   If the object's color is red (2):
        *   Check if the object is adjacent (horizontally or vertically) to *another* object of color red (2).
        *   If it *is* adjacent to another red (2) object, change all pixels within the object to yellow (4).

4.  **Preservation:** All other objects maintain their colors and positions.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in the grid, excluding color 0."""
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
                if current_object:
                    objects.append((grid[r,c], current_object)) # Store color and object pixels
    return objects

def is_adjacent_to_object_of_color(grid, object_pixels, color, objects):
    """Checks if an object is adjacent to another object of a specific color."""
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    for r, c in object_pixels:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc):
                for other_color, other_object_pixels in objects:
                    if other_color == color and (nr, nc) in other_object_pixels and other_object_pixels != object_pixels:
                        return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Iterate through all objects found
    for color, object_pixels in objects:
        # Ignore color 7
        if color == 7:
            continue

        # Red (2) Object Transformation
        if color == 2:
            adjacent_to_red = is_adjacent_to_object_of_color(input_grid, object_pixels, 2, objects)

            if adjacent_to_red:
                for r, c in object_pixels:
                    output_grid[r, c] = 4

    return output_grid
```