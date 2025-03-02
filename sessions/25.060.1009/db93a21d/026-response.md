# db93a21d • 026 • refine_coder

---
```python
"""
1.  **Identify Maroon Regions:** Locate all contiguous regions of maroon (9) pixels.
2.  **Green Fill:**
    *   Find the leftmost maroon region.
    *   Replace all maroon pixels of that region with green pixels.
    *   Flood fill white pixels connected to these new green pixels with green.
3.  **Blue Outline (Conditional):**
    *   If other maroon objects exist, identify them
    *   Check if these other maroon objects are adjacent (above or below) a green object
    *   If so, replace the white outline of the maroon object with blue.
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

def flood_fill(grid, start_pixels, new_color):
    """Fills a connected region with the new color, starting from multiple seed pixels."""
    if not start_pixels:
        return grid
    rows, cols = grid.shape
    old_color = grid[start_pixels[0][0], start_pixels[0][1]] # Get color from first pixel

    visited = np.zeros_like(grid, dtype=bool)
    queue = start_pixels.copy()

    while queue:
        row, col = queue.pop(0)
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != old_color):
            continue

        visited[row, col] = True
        grid[row, col] = new_color

        queue.append((row + 1, col))
        queue.append((row - 1, col))
        queue.append((row, col + 1))
        queue.append((row, col - 1))
    return grid

def get_outline(grid, object_pixels, old_color, new_color):
    """Replace the outline of an object with a new color."""
    rows, cols = grid.shape
    for r, c in object_pixels:
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == old_color:
                grid[nr, nc] = new_color
    return grid

def is_adjacent_to_green(grid, maroon_object):
    """Check if the maroon object is adjacent to a green object (above or below)."""
    rows, cols = grid.shape
    for r, c in maroon_object:
        # Check above and below neighbors
        neighbors = [(r - 1, c), (r + 1, c)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 3:
                return True
    return False

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all maroon objects.
    maroon_objects = find_objects(output_grid, 9)

    # Green Fill (Leftmost Region)
    leftmost_maroon_object = get_leftmost_object(maroon_objects)
    if leftmost_maroon_object:
        # Replace maroon with green
        for row, col in leftmost_maroon_object:
            output_grid[row, col] = 3  # Green

        # Flood fill connected white pixels with green, starting from the newly green pixels
        green_pixels = [(r, c) for r, c in leftmost_maroon_object]
        white_neighbors = []
        rows, cols = output_grid.shape
        for r,c in green_pixels:
            neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            for nr, nc in neighbors:
                if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr,nc] == 0:
                    white_neighbors.append((nr,nc))

        output_grid = flood_fill(output_grid, white_neighbors, 3)

    # Blue outline (Conditional)
    if len(maroon_objects) > 1:  # Check if other maroon objects exist
        for maroon_obj in maroon_objects:
            if maroon_obj != leftmost_maroon_object:  # Check all except the one just filled
                if is_adjacent_to_green(output_grid, maroon_obj):
                    output_grid = get_outline(output_grid, maroon_obj, 0, 1)

    return output_grid
```
