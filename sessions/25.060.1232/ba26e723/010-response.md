# ba26e723 • 010 • example_2 • investigate_coder

---
```python
"""
Finds corners of white (0) pixel regions and changes the yellow (4) pixels at those corners to magenta (6).
"""

import numpy as np

def find_white_corners(input_grid):
    # Find coordinates of white pixels
    white_coords = np.argwhere(input_grid == 0)
    corners = []
    for r, c in white_coords:
      #define corners based on 2x2 areas surrounding white pixels.
        if r > 0 and c > 0:
            corners.append((r - 1, c - 1))  # Upper-left
        if r > 0 and c < input_grid.shape[1] - 1:
            corners.append((r - 1, c + 1))  # Upper-right
        if r < input_grid.shape[0] - 1 and c > 0:
            corners.append((r + 1, c - 1))  # Lower-left
        if r < input_grid.shape[0] - 1 and c < input_grid.shape[1] - 1:
            corners.append((r + 1, c + 1))  # Lower-right
    return corners

def transform(input_grid):
    """
    Transforms the input grid by changing yellow pixels at the corners of white regions to magenta.
    """
    output_grid = np.copy(input_grid)
    corners = find_white_corners(input_grid)

    # Change yellow corners to magenta
    for r, c in corners:
        if output_grid[r,c] == 4:
            output_grid[r, c] = 6

    return output_grid
```
