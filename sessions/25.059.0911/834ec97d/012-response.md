# 834ec97d • 012 • refine_coder

---
```python
"""
1.  **Check for Center:** Determine if a magenta (6) pixel exists in the input grid. If it doesn't exist, make the entire output grid white (0).
2.  **Draw Top Line:** If the magenta pixel exists, draw a horizontal line of yellow (4) pixels across the entire first row of the grid, replacing only white (0) pixels.
3.  **Draw other Lines**: draw a horizontal line of yellow (4) pixels, the same width of the grid, replacing only white (0) pixels in the input.
"""

import numpy as np

def find_center_pixel(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]  # Return the first occurrence
    return None

def transform(input_grid):
    output_grid = np.zeros_like(input_grid) # Initialize to all white (0)
    rows, cols = input_grid.shape
    center_coords = find_center_pixel(input_grid, 6)

    if center_coords:
        # Draw Top Line (replacing only white pixels)
        for c in range(cols):
            if input_grid[0, c] == 0:
                output_grid[0, c] = 4

        # Draw all other lines (replacing only white pixels)
        for r in range(rows):
            for c in range(cols):
                if input_grid[r,c] == 0:
                    output_grid[r,c] = 4


    return output_grid
```

