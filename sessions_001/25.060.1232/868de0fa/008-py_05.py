"""
1.  **Identify Blue Objects:** Find all contiguous regions of blue pixels in the input grid.  Contiguous means connected directly up, down, left, or right (not diagonally).

2.  **Identify Interior Pixels:** For each blue object, determine its interior pixels.  An interior pixel is a blue pixel where all four adjacent pixels (up, down, left, right) are also blue and part of the *same* object.

3.  **Determine Overall Change:** If *any* blue object has interior pixels then continue, otherwise there is no change

4. **Determine Quadrant:** If *any* blue object lies even partially in the top-left quadrant (where row index < rows // 2 and column index < cols // 2) record this fact.

5.  **Apply Color Transformation to Interior Pixels:**
    *   If any blue object had one or more interior pixels, and any part of any blue object is in the top-left quadrant, change the interior pixels of *all* blue objects to red (2).
    *   Otherwise, If any blue object had one or more interior pixels, and no part of any blue object is in the top-left quadrant, change the *all* interior pixels of *all* blue objects to orange (7).
    *   All other pixels remain unchanged.

6.  **Output:** The modified grid is the final output.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous regions (objects) of a specific color in the grid.
    Uses depth first search (DFS), but only considers directly adjacent neighbors.
    """
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        # Check only 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_interior_pixels(grid, object_pixels):
    """
    Identifies the interior pixels of a given object.
    """
    interior_pixels = set()
    for r, c in object_pixels:
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        is_interior = True
        for nr, nc in neighbors:
            if not (0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and (nr, nc) in object_pixels):
                is_interior = False
                break
        if is_interior:
            interior_pixels.add((r, c))
    return interior_pixels

def is_in_top_left_quadrant(grid, object_pixels):
    """
    Checks if any part of an object is in the top-left quadrant of the grid.
    """
    rows, cols = grid.shape
    quadrant_row_limit = rows // 2
    quadrant_col_limit = cols // 2
    for r, c in object_pixels:
        if r < quadrant_row_limit and c < quadrant_col_limit:
            return True
    return False

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()

    # Find blue objects
    blue_objects = find_objects(input_grid, 1)

    # Find interior pixels for all objects
    all_interior_pixels = set()
    has_interior_pixels = False
    for obj in blue_objects:
        interior_pixels = get_interior_pixels(input_grid, obj)
        all_interior_pixels.update(interior_pixels)
        if interior_pixels:
            has_interior_pixels = True

    # If no objects have interior pixels, return the original grid
    if not has_interior_pixels:
        return output_grid

    # Determine if any object is in the top-left quadrant
    any_in_top_left = False
    for obj in blue_objects:
        if is_in_top_left_quadrant(input_grid, obj):
            any_in_top_left = True
            break

    # Apply color transformation based on quadrant and interior pixels
    if any_in_top_left:
        for r, c in all_interior_pixels:
            output_grid[r, c] = 2  # Red
    else:
        for r, c in all_interior_pixels:
            output_grid[r, c] = 7  # Orange

    return output_grid