# e3497940 • 008 • refine_coder

---
```python
"""
1.  **Identify** all gray (5) pixels.
2.  **Identify** all colored pixels (non-black, non-gray) that are directly adjacent (up, down, left, or right) to any gray pixel.
3.  **Remove** all gray pixels.
4.  **Remove** any colored pixels identified in step 2 (adjacent to gray).
5. **Retain** all other pixels (black and any colored pixels not adjacent to gray), maintaining their relative positions. Black pixels (0) act like a background and are unaffected.
6.  The output is a new grid formed by the remaining pixels.
"""

import numpy as np

def find_gray_pixels(grid):
    # Find the row and column indices of all gray (5) pixels.
    gray_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 5:
                gray_pixels.append((r, c))
    return gray_pixels

def find_adjacent_colored_pixels(grid, gray_pixels):
    # Find all colored pixels adjacent to gray pixels.
    adjacent_colored_pixels = set()
    for r, c in gray_pixels:
        # Check neighbors (up, down, left, right)
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                if grid[nr, nc] != 0 and grid[nr, nc] != 5:
                    adjacent_colored_pixels.add((nr, nc))
    return list(adjacent_colored_pixels)

def transform(input_grid):
    # Find all gray pixels
    gray_pixels = find_gray_pixels(input_grid)

    # Find all colored pixels adjacent to gray pixels
    adjacent_colored_pixels = find_adjacent_colored_pixels(input_grid, gray_pixels)

    # Create a list to store the pixels to keep
    pixels_to_keep = []

    # Iterate through the original grid and add non-gray, non-adjacent pixels to keep_pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if (r, c) not in gray_pixels and (r, c) not in adjacent_colored_pixels:
                pixels_to_keep.append((r, c, input_grid[r, c]))

    # Determine the new grid dimensions
    if not pixels_to_keep:
        # Return empty grid, if nothing to show
        return np.zeros((0,0), dtype=int)

    max_row = max(p[0] for p in pixels_to_keep)
    max_col = max(p[1] for p in pixels_to_keep)

    # create mapping of old to new column
    col_map = {}
    new_col = 0
    for c in range(input_grid.shape[1]): # original
        # check if column has a pixel
        keep_col = False
        for r in range(input_grid.shape[0]):
             if (r,c,input_grid[r,c]) in pixels_to_keep:
                keep_col = True
                break
        if keep_col:
            col_map[c] = new_col
            new_col += 1

    # Create the output grid
    output_grid = np.zeros((max_row + 1, new_col), dtype=int)

    # Copy the pixels to keep to the new grid
    for r, c, color in pixels_to_keep:
        output_grid[r, col_map[c]] = color

    return output_grid
```
