"""
1.  **Identify Objects:** Locate all contiguous blocks of pixels with the same color within the input grid.
2.  **Select Target Object:** Select the object with color 2 (red).
3.  **Determine Bounding Box:** Find the smallest rectangle that contains the entirety of the red object. The top-left coordinate will determine the output size, starting from 0,0.
4. **Extract and Transform:** Create a new grid (the output grid) with dimensions relative to the target object. Copy only the red object's pixels to the output grid, maintaining their relative positions. This is, in essence, cropping and extracting the sub-grid defined by the object
5.  **Discard Other Objects:** Ignore all objects that are not red.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if obj_coords:
                    objects.append((color, obj_coords))
    return objects

def bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    min_r = min(r for r, _ in coords)
    max_r = max(r for r, _ in coords)
    min_c = min(c for _, c in coords)
    max_c = max(c for _, c in coords)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    # Find all objects
    objects = find_objects(input_grid)

    # Select the red object (color 2)
    red_object = None
    for color, coords in objects:
        if color == 2:
            red_object = coords
            break

    if red_object is None:
        return np.zeros((0, 0), dtype=int)  # Return empty grid if no red object

    # Determine the bounding box
    min_r, min_c, max_r, max_c = bounding_box(red_object)

    # calculate output grid dimensions
    output_height = max_r - min_r + 1
    output_width = max_c - min_c + 1

    # Create an output grid filled with 0s (background)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Extract and transform the red object onto the output grid
    for r, c in red_object:
        output_grid[r - min_r, c - min_c] = 2

    return output_grid