```python
"""
1.  **Initialize:** Create a 3x3 output grid filled with black (0).
2.  **Find Primary Object:** Locate the top-leftmost non-zero pixel in the input grid. This pixel's color is the "primary color". If there is no such pixel, return output grid..
3.  **Trace Outline**: Find the outline of the connected component. Iterate over all non-zero pixels.
    - Check each non-zero pixel, is it the primary color?
      - If yes, check neighbors (including diagonals):
        - Is any neighbor a different color (or zero)?
          - If yes, this is an outline pixel.
4.  **Normalize and Render:** Create a list of outline pixels `(row, col)`.
    - Find the minimum row (`min_row`) and minimum column (`min_col`) among the outline pixels.
    - Iterate over the outline pixels, `(r, c)`
      - Calculate normalized coordinates `(nr, nc)`:
        - `nr = r - min_row`
        - `nc = c - min_col`
      - if `nr < 3 and nc < 3`: set output[nr, nc] = primary_color
5.  **Return:** Return the 3x3 output grid.
"""

import numpy as np

def find_top_left_non_zero_pixel(grid):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return r, c
    return None, None

def get_neighbors(grid, row, col):
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def is_outline(grid, row, col, primary_color):
    if grid[row, col] != primary_color:
        return False
    for nr, nc in get_neighbors(grid, row, col):
        if grid[nr, nc] != primary_color:
            return True
    return False

def trace_outline(grid, primary_color):
    outline_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if is_outline(grid, r, c, primary_color):
                outline_pixels.append((r, c))
    return outline_pixels

def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros((3, 3), dtype=int)
    input_grid = np.array(input_grid)

    # Find the top-leftmost non-zero pixel and primary color
    start_row, start_col = find_top_left_non_zero_pixel(input_grid)
    if start_row is None:
        return output_grid

    primary_color = input_grid[start_row, start_col]

    # Trace the outline
    outline_pixels = trace_outline(input_grid, primary_color)

    # Normalize and render the outline
    if outline_pixels:
        min_row = min(r for r, _ in outline_pixels)
        min_col = min(c for _, c in outline_pixels)

        for r, c in outline_pixels:
            nr, nc = r - min_row, c - min_col
            if 0 <= nr < 3 and 0 <= nc < 3:
                output_grid[nr, nc] = primary_color

    return output_grid
```