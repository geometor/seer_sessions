# 1e32b0e9 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify horizontal and vertical lines of red (2) pixels.
2. Identify clusters of blue (1) pixels.
3. For each blue pixel, change any directly adjacent (up, down, left, right) red pixel to white (0).
4. Propagate blue color on red pixels if they are connected to other blue pixels
5. Preserve red line and overwrite previous rule at the intersection with a blue cluster
"""

import numpy as np
from scipy.ndimage import label, find_objects

def get_neighbors(r, c, grid_shape):
    """Returns the valid neighbors of a cell in a grid."""
    rows, cols = grid_shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors
  
def get_8_way_connected_neighbors(r,c,grid_shape):
    rows, cols = grid_shape
    neighbors = []
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr,nc))
    return neighbors
    

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify blue pixels and their connected components
    blue_pixels = np.where(input_grid == 1)
    blue_coords = list(zip(blue_pixels[0], blue_pixels[1]))

    # Find connected components of blue pixels
    blue_mask = (input_grid == 1).astype(int)
    labeled_blue, num_blue_features = label(blue_mask)


    # 2. Modify red pixels near blue pixels and propagate blue
    for i in range(1,num_blue_features+1):
        object_slices = find_objects(labeled_blue == i)
        for r,c in np.ndindex(object_slices[0][0].stop - object_slices[0][0].start , object_slices[0][1].stop - object_slices[0][1].start):
             real_r = r + object_slices[0][0].start
             real_c = c + object_slices[0][1].start
             if labeled_blue[real_r,real_c] == i :

                for nr,nc in get_8_way_connected_neighbors(real_r, real_c, (rows,cols)):
                     if output_grid[nr,nc] == 2:
                            output_grid[nr,nc] = 1

    for r, c in blue_coords:
        for nr, nc in get_neighbors(r, c, (rows, cols)):
            if output_grid[nr, nc] == 2:
                output_grid[nr, nc] = 0

    return output_grid
```
