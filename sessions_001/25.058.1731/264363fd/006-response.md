# 264363fd • 006 • refine_coder

---
```python
"""
1.  **Identify the Border:** Find the rectangular region enclosed by Azure (8) pixels. This defines the "interior" region.
2.  **Locate Start Pixels:** Within the interior, locate all Green (3) pixels. These are the starting points for the transformation.
3.  **Constrained Flood Fill:** Starting from each Green pixel, perform a flood fill operation using Red (2) as the fill color.
4.  **Boundary Conditions:** The flood fill should stop when it encounters either an Azure (8) pixel (the border) or an existing Red (2) pixel. The Azure border pixels themselves remain unchanged. The fill extends in all four cardinal directions (up, down, left, right).
"""

import numpy as np

def find_interior(grid, border_color=8):
    """
    Finds the coordinates of the interior region bounded by a border color.
    Assumes a rectangular border.
    """
    rows, cols = grid.shape
    interior_coords = []

    # Find top-left and bottom-right corners of the interior
    top_left = None
    bottom_right = None

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != border_color:
                top_left = (r, c)
                break
        if top_left:
            break

    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] != border_color:
                bottom_right = (r, c)
                break
        if bottom_right:
            break
    
    if not top_left or not bottom_right:
        return []

    for r in range(top_left[0], bottom_right[0] + 1):
        for c in range(top_left[1], bottom_right[1] + 1):
            interior_coords.append((r, c))

    return interior_coords

def constrained_flood_fill(grid, start_coords, fill_color=2, border_color=8, stop_color=2):
    """
    Performs a constrained flood fill operation.

    Args:
        grid: The numpy array representing the grid.
        start_coords: A list of (row, col) tuples representing the starting points for the flood fill.
        fill_color: The color to use for the flood fill (default: red, 2).
        border_color: The color of the border that stops the flood fill (default: azure, 8).
        stop_color: Additional color which stops flood_fill
    Returns:
        A new grid with the flood fill applied.
    """
    rows, cols = grid.shape
    new_grid = np.copy(grid)
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def fill(r, c):
        if (r, c) in visited or not is_valid(r, c) or new_grid[r,c] == border_color or new_grid[r,c] == stop_color:
            return

        visited.add((r, c))
        new_grid[r, c] = fill_color

        fill(r + 1, c)
        fill(r - 1, c)
        fill(r, c + 1)
        fill(r, c - 1)

    for r, c in start_coords:
         if is_valid(r,c) and grid[r,c] != border_color and grid[r,c] != stop_color:
            fill(r,c)

    return new_grid


def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the interior coordinates
    interior_coords = find_interior(output_grid)

    #find green pixels
    green_pixels = []
    for r,c in interior_coords:
        if output_grid[r,c] == 3:
            green_pixels.append((r,c))

    # Perform constrained flood fill, starting from the green pixels
    output_grid = constrained_flood_fill(output_grid, green_pixels)

    return output_grid
```
