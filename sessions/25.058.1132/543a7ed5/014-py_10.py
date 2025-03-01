"""
1.  **Identify Magenta Regions:** Find all connected regions of magenta (6) pixels in the input grid.
2.  **Outline with Green:** Replace all azure (8) pixels directly adjacent to the *exterior* of any magenta region with green (3) pixels.
3. **Fill with yellow where one-pixel boundary:** For each magenta region, check one-pixel-wide internal boundary. If a magenta pixel is next to a newly green pixel, change it to yellow.
4.  **Leave Remaining Pixels:** Any pixels not affected by the above rules retain their original color from the input grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def get_neighbors(grid, r, c):
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0) or (r + i < 0) or (c+j < 0) or (r + i >= rows) or (c + j >= cols):
                continue

            neighbors.append((r + i, c + j))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Magenta Regions
    magenta_mask = (input_grid == 6)
    labeled_magenta, num_magenta_regions = label(magenta_mask)

    # 2. Outline with Green
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:  # Check azure pixels
                neighbors = get_neighbors(input_grid, r, c)
                for nr, nc in neighbors:
                    if input_grid[nr, nc] == 6:  # Adjacent to magenta
                        output_grid[r, c] = 3  # Change to green
                        break  # Once changed to green, no need to check other neighbors

    # 3. Fill with yellow where one-pixel boundary
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 6: #if magenta
                neighbors = get_neighbors(output_grid, r, c)
                for nr, nc in neighbors:
                    if output_grid[nr,nc] == 3: #if adj to green
                        output_grid[r,c] = 4 #change to yellow

    return output_grid