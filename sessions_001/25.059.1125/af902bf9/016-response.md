# af902bf9 • 016 • example_3 • investigate_coder

---
```python
"""
Transforms an input grid by replacing certain white (0) pixels with red (2) pixels based on the arrangement of yellow (4) pixels.  Yellow pixels in the top half with horizontal neighbors have a red pixel inserted between. Yellow pixels in the bottom half with vertical neighbors have a 2x4 red block inserted between.
"""

import numpy as np

def get_yellow_pixels(grid):
    """Finds the coordinates of all yellow (4) pixels."""
    return np.argwhere(grid == 4)

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    yellow_pixels = get_yellow_pixels(input_grid)
    rows, cols = input_grid.shape

    for r, c in yellow_pixels:
        # Horizontal Expansion (Top Half)
        if r < rows / 2:
            if c > 0 and input_grid[r, c-1] == 4:
                output_grid[r,c-1] = 0
                output_grid[r,c] = 4

            if c > 0 and input_grid[r, c-1] == 0 and input_grid[r,c+1] == 4:
                output_grid[r, c] = 4
                output_grid[r,c+1] = 4
                output_grid[r,c-1:c] = [2]
            if c < cols - 1 and input_grid[r, c+1] == 4 :
                output_grid[r,c+1] = 4


        # Vertical Expansion (Bottom Half)
        elif r >= rows / 2:

            if r < rows - 1 and input_grid[r+1, c] == 4: #adjacent yellow pixel below
                output_grid[r+1,c] = 4

            if r < rows - 1 and input_grid[r+1, c] == 0:
              output_grid[r:r+1,c] = [4]

              output_grid[r+1:r+2,c] = [4]
              output_grid[r+1:r-1:-1, c:c+4] = [[2, 2, 2, 2]] #2x4 red block

    return output_grid
```
