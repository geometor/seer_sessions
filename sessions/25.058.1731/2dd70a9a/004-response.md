# 2dd70a9a • 004 • example_1 • investigate_coder

---
```python
"""
Identify green (3) pixels. Expand the green color into adjacent white (0) pixels,
but only within regions not fully enclosed by azure (8) pixels. This expansion
continues iteratively until no green pixels are adjacent to white pixels
within the un-enclosed azure regions.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the row, col coordinates of all pixels of a given color."""
    return np.argwhere(grid == color)

def get_neighbors(grid, row, col):
    """Gets the valid neighbors (up, down, left, right) of a pixel."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def is_fully_enclosed(grid, color):
    """
    Checks if an azure region is fully enclosed by checking for edge contact.  A
    better approach is to flood fill from the edges.
    """
    rows, cols = grid.shape
    pixels = find_pixels_by_color(grid, color)
    for r, c in pixels:
      if r == 0 or r == rows - 1 or c == 0 or c == cols-1:
          return False

    return True



def transform(input_grid):
    """Transforms the input grid according to the expansion rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find largest open azure area.
    if is_fully_enclosed(input_grid, 8):
        return output_grid # no changes if enclosed

    green_pixels = find_pixels_by_color(output_grid, 3)
    if len(green_pixels) == 0:
      return output_grid

    while True:
        new_green_pixels = []
        pixels_to_change = []

        for r, c in green_pixels:
            neighbors = get_neighbors(output_grid, r, c)
            for nr, nc in neighbors:
                if output_grid[nr, nc] == 0:
                    pixels_to_change.append( (nr,nc) )

        if len(pixels_to_change) == 0:
            break;

        for (r,c) in pixels_to_change:
            output_grid[r,c] = 3
            new_green_pixels.append( (r, c) )

        green_pixels = new_green_pixels


    return output_grid
```
