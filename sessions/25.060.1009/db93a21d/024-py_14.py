"""
1.  **Identify Maroon Regions:** Locate all contiguous regions of maroon (9) pixels.
2.  **Green Fill:**
    *   Find the leftmost maroon region.
    *   Replace all maroon pixels of that region by green pixels.
    *   Find connected white region to the identified maroon region, that also touch the top edge of the grid
    *   Replace pixels in that white region with green.
3.  **Blue Outline(Conditional):**
    *   If exists a maroon object located directly under an object that was colored green, replace white border for that object with blue color.
4. **Unchanged:** If other maroon regions exists they are not changed.
"""

import numpy as np

def find_objects(grid, color):
    """Find contiguous regions of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        object_pixels = [(row, col)]

        object_pixels.extend(dfs(row + 1, col))
        object_pixels.extend(dfs(row - 1, col))
        object_pixels.extend(dfs(row, col + 1))
        object_pixels.extend(dfs(row, col - 1))
        return object_pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                objects.append(dfs(row, col))
    return objects

def get_leftmost_object(objects):
    """Returns the object with the smallest col index (left-most)."""
    if not objects:
        return None
    return min(objects, key=lambda obj: min(pixel[1] for pixel in obj))

def flood_fill(grid, start_row, start_col, new_color):
    """Fills a connected region with the new color."""
    rows, cols = grid.shape
    old_color = grid[start_row, start_col]
    if old_color == new_color:
        return

    def dfs(row, col):
        if 0 <= row < rows and 0 <= col < cols and grid[row, col] == old_color:
            grid[row, col] = new_color
            dfs(row + 1, col)
            dfs(row - 1, col)
            dfs(row, col + 1)
            dfs(row, col - 1)

    dfs(start_row, start_col)
    return grid

def get_outline(grid, object_pixels, old_color, new_color):
    """Replace the outline of an object with a new color."""
    rows, cols = grid.shape

    for r, c in object_pixels:
        neighbors = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
        for nr, nc in neighbors:
             if 0 <= nr < rows and 0 <= nc < cols and grid[nr,nc] == old_color:
                 grid[nr,nc] = new_color

    return grid

def is_below_green(grid, maroon_object):
    """Check if any pixel in the object is directly under a green pixel."""
    for r, c in maroon_object:
        if r > 0 and grid[r-1, c] == 3:
            return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all maroon objects.
    maroon_objects = find_objects(output_grid, 9)

    # Green Fill (Leftmost Region)
    leftmost_maroon_object = get_leftmost_object(maroon_objects)
    if leftmost_maroon_object:
        #replace maroon by green
        for row, col in leftmost_maroon_object:
            output_grid[row, col] = 3  # Green

        #fill connected white, that touch top edge
        for c in range(output_grid.shape[1]):
           flood_fill(output_grid,0,c,3)

    # Blue outline (Conditional)
    if len(maroon_objects) > 1: # Check if other maroon object exists
      for maroon_obj in maroon_objects:
        if maroon_obj != leftmost_maroon_object: # Check all except the one just filled
             if is_below_green(output_grid, maroon_obj):
                 output_grid = get_outline(output_grid, maroon_obj, 0, 1)

    return output_grid