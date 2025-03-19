# 39a8645d • 012 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to extract the yellow (4) pixels from the input grid and represent their relative positions within a 3x3 output grid, maintaining the shape of contiguous yellow pixels. All other colors are ignored, and the background of the output grid is white (0).
"""

import numpy as np

def find_yellow_blobs(grid):
    """Finds all contiguous blobs of yellow (4) pixels in the grid."""
    yellow_pixels = np.argwhere(grid == 4)
    blobs = []
    visited = set()

    def dfs(r, c, current_blob):
        if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != 4:
            return
        visited.add((r, c))
        current_blob.append((r, c))
        dfs(r + 1, c, current_blob)
        dfs(r - 1, c, current_blob)
        dfs(r, c + 1, current_blob)
        dfs(r, c - 1, current_blob)

    for r, c in yellow_pixels:
        if (r, c) not in visited:
            current_blob = []
            dfs(r, c, current_blob)
            blobs.append(current_blob)
    return blobs

def transform(input_grid):
    """Transforms the input grid by extracting yellow pixels and placing them in a 3x3 output grid."""

    # Find yellow blobs
    yellow_blobs = find_yellow_blobs(input_grid)

    # Initialize output grid (3x3, filled with 0)
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Find min and max row/col for yellow pixels to calculate relative position.
    if yellow_blobs:
        all_yellow_pixels = [pixel for blob in yellow_blobs for pixel in blob]
        min_row = min(pixel[0] for pixel in all_yellow_pixels)
        max_row = max(pixel[0] for pixel in all_yellow_pixels)
        min_col = min(pixel[1] for pixel in all_yellow_pixels)
        max_col = max(pixel[1] for pixel in all_yellow_pixels)

        row_range = max_row - min_row + 1
        col_range = max_col - min_col + 1


        for blob in yellow_blobs:
          for r, c in blob:
            # map to output
            out_r = int(((r - min_row) / (row_range -1 )) * 2) if row_range > 1 else 1
            out_c = int(((c - min_col) / (col_range - 1)) * 2) if col_range > 1 else 1

            output_grid[out_r,out_c] = 4

    return output_grid
```
