# 11852cab • 020 • refine_coder

---
```python
"""
1.  **Identify the Blue Pixel (if present):** Search for a single blue (1) pixel within the grid. This pixel acts as the center of a two-fold rotational symmetry. If no blue pixel is found, the grid remains unchanged.

2.  **Identify Adjacent Yellow Pixels:** Locate all yellow (4) pixels directly adjacent to the blue pixel, either horizontally or vertically.

3.  **Duplicate Yellow Pixels Symmetrically:**
    *   For each yellow pixel found adjacent to the blue pixel, create a mirror image of that pixel on the opposite side of the blue pixel, at the same distance.  This mirroring occurs both horizontally and vertically.
    *   If a mirrored position is occupied by a yellow pixel in the input, the mirrored position remains a yellow pixel.
    *   Only yellow pixels adjacent to the blue pixel are mirrored.

4.  **Preserve Other Pixels:**  All pixels that are not yellow and adjacent to the blue pixel retain their original values.
"""

import numpy as np

def find_pixel_by_color(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size > 0:
        return coords[0]  # return first in list
    return None

def get_adjacent_yellow_pixels(grid, row_b, col_b):
    # Get yellow pixels directly adjacent (horizontally/vertically) to the blue pixel.
    rows, cols = grid.shape
    adjacent_yellows = []

    # Check up, down, left, and right
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_r, new_c = row_b + dr, col_b + dc
        if 0 <= new_r < rows and 0 <= new_c < cols and grid[new_r, new_c] == 4:
            adjacent_yellows.append((new_r, new_c))
    return adjacent_yellows

def duplicate_yellow_symmetrically(grid, blue_coords):
    # Duplicate yellow pixels symmetrically across the blue pixel (both horizontally and vertically).
    output_grid = np.copy(grid)
    row_b, col_b = blue_coords
    adjacent_yellows = get_adjacent_yellow_pixels(grid, row_b, col_b)
    rows, cols = grid.shape

    for r, c in adjacent_yellows:
        # Mirror horizontally
        new_c = col_b - (c - col_b)
        if 0 <= new_c < cols:
            output_grid[r, new_c] = 4

        # Mirror vertically
        new_r = row_b - (r - row_b)
        if 0 <= new_r < rows:
            output_grid[new_r, c] = 4

    return output_grid

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the blue pixel
    blue_coords = find_pixel_by_color(output_grid, 1)

    # If blue exists, apply duplication
    if blue_coords is not None:
        output_grid = duplicate_yellow_symmetrically(output_grid, blue_coords)

    return output_grid
```
