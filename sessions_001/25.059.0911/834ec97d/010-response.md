# 834ec97d • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Locate Center:** Find the magenta (6) pixel in the input grid. This is the center (row 2, col 2 considering 0 based indexing).
2.  **Draw above**: move up three rows, then draw a line of yellow (4) pixels the same width as the grid.
3.  **Draw Middle**: draw two rows up from the center, a line of yellow (4), replacing white (0) and leaving other colors unchanged.
4.  **Keep Center:** Maintain the magenta (6) pixel at its original location.
5. **Leave the rest**: Leave everything else as white (0)
"""

import numpy as np

def find_center_pixel(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]  # Return the first occurrence
    return None

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_coords = find_center_pixel(input_grid, 6)

    if center_coords:
        center_row, center_col = center_coords

        # Draw above
        output_grid[0, :] = [4 if x == 0 else x for x in output_grid[0,:]]

        # Draw Middle (two rows above center)
        if center_row >= 2:
          output_grid[center_row-2, :] = [4 if x == 0 else x for x in  output_grid[center_row - 2,:] ]


    return output_grid
```
