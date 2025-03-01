"""
1.  **Identify Objects:** Find all rectangular objects of color green (3) and magenta (6).
2.  **Iterate Green Objects:** For each green object:
    *   **Find Inner Magenta:** Locate a magenta object that is *within* the bounding box of the current green object. In this case, "inside" means the magenta object shares one complete edge and is otherwise within the green object, but not equal.
    * **Color Swap Row-wise:**
      *   Within the row(s) occupied by the magenta object inside the current green one, swap all magenta (6) pixels to green (3).
      *   Within the rows occupied by the green object, *excluding* the magenta object's row(s), swap all green (3) pixels to magenta (6).
"""

import numpy as np

def find_objects(grid, color):
    """Finds all rectangular objects of the specified color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                if current_object:
                    min_row = min(cell[0] for cell in current_object)
                    max_row = max(cell[0] for cell in current_object)
                    min_col = min(cell[1] for cell in current_object)
                    max_col = max(cell[1] for cell in current_object)
                    objects.append(((min_row, min_col), (max_row, max_col)))
    return objects

def is_inside(inner_object, outer_object):
    """Checks if inner_object is inside outer_object and shares at least one full edge."""
    outer_top, outer_bottom = outer_object
    inner_top, inner_bottom = inner_object
    
    if not (outer_top[0] <= inner_top[0] and inner_bottom[0] <= outer_bottom[0] and
            outer_top[1] <= inner_top[1] and inner_bottom[1] <= outer_bottom[1]):
        return False
    
    # Check for at least one shared edge (top, bottom, left, or right)
    if (inner_top[0] == outer_top[0] or inner_bottom[0] == outer_bottom[0] or
        inner_top[1] == outer_top[1] or inner_bottom[1] == outer_bottom[1]):
      
        return True

    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find all green and magenta objects
    green_objects = find_objects(input_grid, 3)
    magenta_objects = find_objects(input_grid, 6)

    # Iterate through green objects
    for green_object in green_objects:
        green_top, green_bottom = green_object

        # Find a magenta object inside the current green object
        for magenta_object in magenta_objects:
            if is_inside(magenta_object, green_object):
                magenta_top, magenta_bottom = magenta_object

                # Swap colors row-wise
                for r in range(green_top[0], green_bottom[0] + 1):
                    if magenta_top[0] <= r <= magenta_bottom[0]:
                        # Rows of magenta object: swap magenta to green
                        for c in range(green_top[1], green_bottom[1] + 1):
                            if output_grid[r, c] == 6:
                                output_grid[r, c] = 3
                    else:
                        # Rows of green object, excluding magenta: swap green to magenta
                        for c in range(green_top[1], green_bottom[1] + 1):
                            if output_grid[r, c] == 3:
                                output_grid[r, c] = 6
                break  # Assume only one magenta object per green object.

    return output_grid