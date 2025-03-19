# d2abd087 • 006 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Gray Objects:** Locate all contiguous regions of gray (5) pixels in the input grid.  "Contiguous" means connected horizontally or vertically.
2.  **Recolor Gray to Red:** Change the color of all identified gray pixels to red (2).
3.  **Identify Adjacent White Pixels:** Find all white (0) pixels that are directly adjacent (left, right, above, or below) to the original gray pixels (now red). It is critical that only the orginal position matters.
4.  **Recolor Adjacent Whites to Blue:** Change the color of these adjacent white pixels to blue (1).
5. All other white pixels are unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        # Check adjacent cells (up, down, left, right)
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_adjacent_pixels(grid, pixel_coords):
    """Gets the coordinates of pixels adjacent to the given pixel."""
    rows, cols = grid.shape
    r, c = pixel_coords
    adjacent = []
    # Check up, down, left, right
    if r > 0:
        adjacent.append((r - 1, c))
    if r < rows - 1:
        adjacent.append((r + 1, c))
    if c > 0:
        adjacent.append((r, c - 1))
    if c < cols - 1:
        adjacent.append((r, c + 1))
    return adjacent

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Gray Objects
    gray_objects = find_objects(input_grid, 5)

    # Store original gray pixel locations for adjacency check
    original_gray_pixels = set()
    for obj in gray_objects:
        for r, c in obj:
          original_gray_pixels.add((r,c))

    # 2. Recolor Gray to Red
    for obj in gray_objects:
        for r, c in obj:
            output_grid[r, c] = 2

    # 3 & 4. Identify and Recolor Adjacent White Pixels to Blue
    for r, c in original_gray_pixels:
        adjacent_pixels = get_adjacent_pixels(input_grid, (r, c))
        for ar, ac in adjacent_pixels:
            if input_grid[ar, ac] == 0:  # Check if it's white in the *input* grid
                output_grid[ar, ac] = 1

    return output_grid
```
