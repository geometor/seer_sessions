# 77fdfe62 • 004 • refine_coder

---
```python
"""
1. **Identify Non-White Pixels:** Locate all pixels within the input grid that are not white (0).

2. **Order Non-White Pixels:** Order these pixels based on their position in the grid. The order is determined by reading the grid in a "Z" pattern: top-left to top-right, then move down to the next non-white pixel to its left or right, and so on, zigzagging down the grid.

3.  **Create Output Grid:** Create a 4x4 output grid.

4.  **Place Extracted Colors:** Populate the output grid sequentially with the colors of the ordered non-white pixels, starting from the top-left cell (0,0) and moving left-to-right, then top-to-bottom. If there are more non-white pixels than cells in the output grid, fill only up to the available slots. If fewer, leave the remaining output grid cells as white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((4, 4), dtype=int)

    # Identify non-white pixels and their positions
    non_white_pixels = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] != 0:
                non_white_pixels.append((r, c, input_grid[r, c]))

    # Sort non-white pixels in Z-order (top-left to right, then zigzag down)
    non_white_pixels.sort(key=lambda x: (x[0], x[1]))
    
    # Populate output grid
    row = 0
    col = 0
    for i in range(len(non_white_pixels)):
      if (row < 4):
        output_grid[row, col] = non_white_pixels[i][2]
        col = col + 1
        if col >= 4:
            col = 0
            row += 1

    return output_grid
```
