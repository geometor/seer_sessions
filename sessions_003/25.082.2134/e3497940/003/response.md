```python
"""
1.  **Find the Gray Line:** Identify the vertical column composed entirely of gray (5) pixels.
2.  **Iterate through pixels left of the gray line:** check pixels in any colored objects.
3.  **Check Adjacency:** For each pixel in objects to the left of the gray line:
    *   Check if the pixel is *directly adjacent* (horizontally or vertically, *not* diagonally) to *any* pixel in the gray line.
    *  If it IS adjacent: Preserve the pixel.
    *  If it is NOT adjacent: remove the pixel.
4.  **Construct Output:** Create a new grid. Copy all preserved adjacent pixels from the objects, maintaining their row positions.
5. **Determine Output width:** the width of the output grid will equal the number of columns between and including the leftmost preserved pixel, and the gray line.
"""

import numpy as np

def find_gray_line(grid):
    """Finds the vertical line of gray (5) pixels."""
    rows, cols = grid.shape
    for j in range(cols):
        is_gray_line = True
        for i in range(rows):
            if grid[i, j] != 5:
                is_gray_line = False
                break
        if is_gray_line:
            return j
    return -1  # Should not happen

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    gray_line_col = find_gray_line(input_grid)

    # Determine output grid width
    max_x = 0
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] != 0 and c < gray_line_col:
                is_adjacent = False
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and nc == gray_line_col and input_grid[nr,nc] == 5:
                        is_adjacent = True
                        break
                if is_adjacent:
                    max_x = max(max_x, c)
    output_grid = np.zeros((input_grid.shape[0], max_x+1), dtype=int)

    # change output pixels - preserve parts of objects
    for r in range(rows):
        for c in range(cols):
          if c < gray_line_col: # only consider objects left to the gray line
            is_adjacent = False
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
              nr, nc = r + dr, c + dc
              if 0 <= nr < input_grid.shape[0] and nc == gray_line_col and input_grid[nr,nc] == 5:
                is_adjacent = True
                break
            if is_adjacent:
              output_grid[r,c] = input_grid[r,c]

    return output_grid.tolist()
```