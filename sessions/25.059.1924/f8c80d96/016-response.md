# f8c80d96 • 016 • refine_coder

---
```python
"""
1.  **Border Identification and Gray Filling**: Identify the outermost rows and columns of the input grid. Change all white (0) pixels in these border rows and columns to gray (5).

2.  **Inverse White to Red:**
    *   Locate all of the Red Pixels, note their position.
    *   Change all remaining white pixels to where red pixels would be if they were in the position of that white pixel.

3.  **Red Preservation:** Do not modify any red pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Border Identification and Gray Filling
    for r in range(rows):
        for c in range(cols):
            if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and output_grid[r, c] == 0:
                output_grid[r, c] = 5

    # Inverse White to Red and Red Preservation
    red_positions = []
    for r in range(rows):
      for c in range(cols):
        if output_grid[r,c] == 2:
          red_positions.append((r,c))

    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                for red_pos in red_positions:
                    inv_r = red_pos[0]
                    inv_c = red_pos[1]
                    if input_grid[r,c] == 0:
                      output_grid[r,c] = 2
                      

    return output_grid
```
