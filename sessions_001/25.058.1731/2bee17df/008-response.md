# 2bee17df • 008 • refine_coder

---
```python
"""
1.  **Identify Objects:** Identify three distinct objects: an irregular "azure_boundary" (color 8), a "red_region" (color 2), and a "green_region" (color 3) that will be created.

2.  **Fill Inside Boundary:** Fill the area enclosed by the `azure_boundary` with green (color 3) to create the `green_region`.

3.  **Red Exclusion:** During the fill operation, any white pixel (color 0) that is directly adjacent (up, down, left, or right) to any pixel in the `red_region` is *not* filled with green. It remains unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Returns a list of neighbors (up, down, left, right) for a given cell."""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def find_object(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    object_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                object_pixels.append((r, c))
    return object_pixels

def is_inside_boundary(grid, row, col, boundary_color):
    """
    Checks if a given cell is inside the boundary defined by the boundary_color.
    Uses a flood-fill algorithm to determine enclosure.
    """
    rows, cols = grid.shape
    if grid[row, col] == boundary_color:
        return False  # On the boundary itself

    visited = set()
    stack = [(row, col)]

    while stack:
        r, c = stack.pop()

        if (r, c) in visited:
            continue
        visited.add((r, c))

        if grid[r,c] == boundary_color:
            continue # hit the boundary, keep going around

        # If we reach the edge of the grid without hitting the boundary color, it's not enclosed
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            return False

        for nr, nc in get_neighbors(grid, r, c):
            if (nr, nc) not in visited:
              stack.append((nr,nc))

    return True

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify Objects
    azure_boundary_pixels = find_object(output_grid, 8)
    red_region_pixels = find_object(output_grid, 2)

    # Fill Inside Boundary, with Red Exclusion
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:  # Consider only white pixels
                if is_inside_boundary(output_grid, r, c, 8):  # Check if inside azure boundary
                    is_adjacent_to_red = False
                    for neighbor_row, neighbor_col in get_neighbors(output_grid, r, c):
                        if (neighbor_row, neighbor_col) in red_region_pixels:
                            is_adjacent_to_red = True
                            break
                    if not is_adjacent_to_red:
                        output_grid[r, c] = 3  # Fill with green

    return output_grid
```
