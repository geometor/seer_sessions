# 1b2d62fb • 024 • refine_coder

---
```python
"""
1.  **Identify Blue Rows:** Examine the input grid to identify all rows that contain at least one blue (1) pixel.
2.  **Determine Output Height:** Count the number of rows identified in step 1. This count will be the height of the output grid.
3.  **Create Output Grid:** Create a new grid with the calculated height and a fixed width of 3. Initialize all pixels in this grid to white (0).
4.  **Place Azure Pixels:** For each row identified in step 1, place an azure (8) pixel in the center column (index 1) of the corresponding row in the output grid.
5.  **Handle Empty Case:** If no rows contain blue pixels, return an empty grid of size 0x3.
"""

import numpy as np

def find_blue_rows(grid):
    # Find the row indices where blue (1) pixels exist
    rows, _ = grid.shape
    blue_rows = []
    for i in range(rows):
        if 1 in grid[i]:
            blue_rows.append(i)
    return blue_rows

def transform(input_grid):
    # Find rows with blue pixels
    blue_rows = find_blue_rows(input_grid)

    # Determine output grid height
    output_height = len(blue_rows)
    
    # Handle Empty Case
    if output_height == 0:
      return np.zeros((0,3),dtype=int)


    # Create Output Grid
    output_grid = np.zeros((output_height, 3), dtype=int)

    # Place Azure Pixels
    for i in range(output_height):
        output_grid[i, 1] = 8

    return output_grid
```

