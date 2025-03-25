"""
1.  **Identify Objects:** Scan the input grid and identify all contiguous blocks of non-zero pixels.  Consider each block as a separate object. Note the color, shape, and position of each object.
2.  **Iterate Through Red (2) Objects:** For each object identified as having the color red (2):
    *   **Check Adjacency to another Red Object:** Check adjacent pixels for any other red objects.
        *   If another red object is adjacent:
            *   **Check adjacent pixels for yellow:** Find adjacent pixels to the initial red object and check if any are yellow.
                *   If yellow is present, keep original red color.
                *   If yellow is not present, change the first red color object to yellow (4).
        *   If not next to red, keep original color.
3.  **Preserve Other Colors:** All other colors, except `7`, remain unchanged, unless they are adjacent to an object of color 7, in which case, it keeps its original color.
4. **Color 7:** Preserve color `7`.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in the grid."""
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
def is_adjacent_to_color(grid, object_pixels, color):
    """Checks if an object is adjacent to a pixel of a specific color."""
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    for r, c in object_pixels:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and grid[nr, nc] == color:
                return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)


    # Iterate through all objects found
    for color, object_pixels in objects:

        # rule for color 7
        if color == 7:
          continue

        if is_adjacent_to_color(input_grid, object_pixels, 7):
          continue # keep color

        # change 2 to 4 given the rule
        if color == 2:
            adjacent_to_red = False
            for other_color, other_object_pixels in objects:
                if other_color == 2 and object_pixels != other_object_pixels:
                    if is_adjacent_to_color(input_grid, object_pixels, 2):
                      adjacent_to_red = True
                      break # another red object is adjacent
            if adjacent_to_red:
                if not is_adjacent_to_color(input_grid,object_pixels, 4):
                    for r, c in object_pixels:
                        output_grid[r, c] = 4

    return output_grid