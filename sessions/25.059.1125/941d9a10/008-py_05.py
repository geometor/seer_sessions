"""
1.  **Identify Gray Lines:** Find the two horizontal and two vertical gray lines. These lines consist of contiguous gray (5) pixels.
2.  **Determine Reference Point:** Define the intersection points of the horizontal and vertical gray lines. These intersections will serve as relative origins for placing the colored regions, even though not all lines always intersect.
3.  **Place Blue Region:** Create a 3x3 blue (1) region.  Its top-left corner is positioned *above and to the left* of the gray lines. Specifically, if the first horizontal gray line is row `r` and the first vertical gray line is column `c`, the top-left of the blue region is at `(r-3, c-3)`. If `r` or `c` is less that 3, start the top-left corner at `(0,0)`.
4.  **Place Red Region:** Create a 3x3 red (2) region. Its top-left corner is positioned to the *bottom-right* of the gray lines intersection, or the *bottom left*, depending on the position of the other vertical gray line. Specifically, if the second horizontal gray line is at row `r`, and a vertical gray line is at column `c`, the red region will begin near `(r+1,c-3)` or near `(r+1, c+1)` depending on context.
5.  **Place Green Region:** Create a 3x3 green (3) region. Its top-left corner is positioned to the *bottom-right* of the second set of gray lines. If the second horizontal line is at `r` and the second vertical line is at `c`, place the top-left corner of this region at `(r+1, c+1)`.
6. **Preserve other white pixels:** All other white pixels that are not gray and not included in colored regions, remain unchanged.
"""

import numpy as np

def find_gray_lines(grid):
    """Finds the rows and columns of gray lines."""
    gray_rows = np.where(np.all(grid == 5, axis=1))[0]
    gray_cols = np.where(np.all(grid == 5, axis=0))[0]
    return gray_rows, gray_cols

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = find_gray_lines(input_grid)

    # Place Blue Region
    r_blue = max(0, rows[0] - 3 if len(rows) > 0 else 0)
    c_blue = max(0, cols[0] - 3 if len(cols) > 0 else 0)
    for i in range(r_blue, min(r_blue + 3, output_grid.shape[0])):
        for j in range(c_blue, min(c_blue + 3, output_grid.shape[1])):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 1
    
    # Place Red Region
    if len(rows) > 1 and len(cols) > 0:
      r_red = rows[1] + 1 if len(rows) > 1 else 0
      # Determine if the vertical line for red should be the first or second, avoid overlap
      c_red = cols[0] + 1 if len(cols) > 0 else 0
      if c_red >= cols[0] and c_red < (cols[0] + 3 if len(cols) > 0 else output_grid.shape[1] - 1) and len(cols) > 1 :
        c_red = cols[1] - 3

      for i in range(r_red, min(r_red + 3, output_grid.shape[0])):
            for j in range(max(0,c_red), min(c_red + 3, output_grid.shape[1])):
                if output_grid[i, j] == 0:
                  output_grid[i, j] = 2
    
    # Place Green Region
    if len(rows) > 1 and len(cols) > 1:
      r_green = rows[1] + 1
      c_green = cols[1] + 1
      for i in range(r_green, min(r_green + 3, output_grid.shape[0])):
          for j in range(c_green, min(c_green + 3, output_grid.shape[1])):
              if output_grid[i, j] == 0:
                output_grid[i, j] = 3

    return output_grid