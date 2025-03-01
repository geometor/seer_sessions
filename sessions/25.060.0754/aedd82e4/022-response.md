# aedd82e4 • 022 • example_4 • investigate_coder

---
```python
"""
1. Preserve Red: Keep all red (value 2) pixels from the input grid in the same positions in the output grid.
2. Center Conversion. If there is a red (value 2) pixel in the direct center of the input grid, then change the pixel value at that location to a 1 (blue) in the output grid.
3. Vertical and Horizontal Change: For the white (value 0) pixels that are vertically or horizontally adjacent to the center pixel, If any are color 0 (white), change to color 1(blue).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the center coordinates
    center_row = rows // 2
    center_col = cols // 2

    #2 & 3. Center and Adjacent Conversion.
    for i in range(rows):
        for j in range(cols):
            if i == center_row and j == center_col:
                if output_grid[i,j] == 2:
                  output_grid[i, j] = 1
            elif (i == center_row and (j == center_col - 1 or j == center_col + 1)) or \
                 (j == center_col and (i == center_row - 1 or i == center_row + 1)):
                if output_grid[i, j] == 0:
                    output_grid[i, j] = 1

    return output_grid
```
