# 83302e8f • 018 • refine_coder

---
```python
"""
1.  **Identify Maroon Boundaries:** Locate all horizontal and vertical lines formed by maroon (9) pixels in the input grid. These lines define the boundaries of enclosed areas.
2.  **Iterate Through Pixels:** Examine each pixel in the grid that is not a maroon pixel (9).
3.  **Determine Fill Color for Current Pixel:**
      - Get the color values of adjacent pixels (up, down, left, and right), stopping the search if a maroon pixel is encountered in that direction.
      - If no colored neighbors are found (only maroon or empty), fill with yellow(4).
      - If only yellow neighbors are found, fill with green(3)
      - If only green neighbors are found, fill with yellow(4).
      - If there are both green and yellow neighbors, do not change the pixel.
4.  **Fill Pixel:** Change the current pixel in the output grid to the determined fill color.
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
