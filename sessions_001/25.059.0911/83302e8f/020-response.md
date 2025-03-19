# 83302e8f • 020 • refine_coder

---
```python
"""
1.  **Identify Maroon Boundaries:** Locate all horizontal and vertical lines formed by maroon (9) pixels in the input grid. These lines define the boundaries of fully enclosed areas.

2.  **Iterate Through Pixels:** Examine each pixel in the grid that is *not* a maroon pixel (9).

3.  **Determine Fill Color:** For the current pixel:
    *   Check adjacent pixels (up, down, left, and right) one step at a time. Stop searching in a direction if a maroon (9) pixel is encountered. Record the color of any non-background and non-maroon pixel first encountered in any direction.
    *   Apply these fill rules:
        *   If *no* colored neighbors are found (only maroon boundary pixels or empty pixels), fill the current pixel with yellow (4).
        *   If *only* yellow (4) neighbors are found, fill the current pixel with green (3).
        *   If *only* green (3) neighbors are found, fill the current pixel with yellow (4).
        *   If a *mix* of green (3) and yellow (4) neighbors is found, *do not change* the current pixel.

4.  **Fill Pixel:** Update the output grid by setting the current pixel to the `fill_color` determined in the previous step. If no change is needed, keep original color.
"""

import numpy as np

def check_neighbors(grid, r, c):
    neighbors = []
    rows, cols = grid.shape
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Left, Right, Up, Down
        nr, nc = r + dr, c + dc
        while 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr, nc] == 9:
                break
            if grid[nr,nc] != 0:
                neighbors.append(grid[nr,nc])
                break
            nr, nc = nr + dr, nc + dc
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # iterate through pixels
    for r in range(rows):
        for c in range(cols):
            # process only if it is not maroon
            if output_grid[r,c] != 9:
                # determine fill color
                neighbors = check_neighbors(output_grid, r, c)
                fill_color = 0 # default, means no change
                if not neighbors:
                    fill_color = 4
                elif all(neighbor == 4 for neighbor in neighbors):
                    fill_color = 3
                elif all(neighbor == 3 for neighbor in neighbors):
                    fill_color = 4

                #fill pixel
                if fill_color != 0:
                    output_grid[r,c] = fill_color
    return output_grid
```
