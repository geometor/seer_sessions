```python
"""
1.  **Grid Division:** Divide the input grid into two halves vertically (top and bottom).
2.  **Identify Top Red Shape:** In the top half of the grid, identify contiguous regions of red pixels. Consider this the "top_red_shape".
3.  **Propagate Red (Outline Extension):** Extend the outline of the top_red_shape by one pixel in all directions (including diagonals) *only if* the adjacent pixel in the original input grid is blue. If a pixel becomes part of this outline extension, its value is changed from blue to red.
4.  **Identify Bottom Red Shape:** In the *original* bottom half, identify regions of red pixels.
5.  **Conditional Removal:** Remove red pixels in the bottom half of the grid that are *not* part of the extended outline created in step 3.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 8 neighbors of a cell (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    mid_row = rows // 2

    # 1. Grid Division: (Implicit in the loop ranges)

    # 2. Identify Top Red Shape: Find red pixels in the top half.
    top_red_pixels = []
    for r in range(0, mid_row):
        for c in range(cols):
            if input_grid[r, c] == 2:
                top_red_pixels.append((r, c))

    # 3. Propagate Red (Outline Extension):
    extended_outline = set()
    for r, c in top_red_pixels:
        neighbors = get_neighbors(input_grid, r, c)
        for nr, nc in neighbors:
            if input_grid[nr, nc] == 1:  # Only propagate to blue pixels
                output_grid[nr, nc] = 2
                extended_outline.add((nr, nc))
        extended_outline.add((r,c)) # add the original pixel

    # add all the original top_red_pixels
    for r,c in top_red_pixels:
        extended_outline.add((r,c))


    # 4. Identify Bottom Red Shape: (Implicit during removal)

    # 5. Conditional Removal:
    for r in range(mid_row, rows):
        for c in range(cols):
            if output_grid[r, c] == 2 and (r, c) not in extended_outline:
                output_grid[r, c] = 0

    return output_grid
```