# dc1df850 • 010 • refine_coder

---
```python
"""
1.  **Identify** all red (color 2) pixels in the input grid.
2.  **If** a red pixel is located on the **top row (row 0)**, create a single blue (color 1) pixel directly to its left.
3.  **Else If** a red pixel in any row except the top row, **create** a 3x3 square of blue (color 1) pixels.
    *   The red pixel will be at the center of the top edge of the blue square.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = input_grid.copy()
    height, width = input_grid.shape

    # Find all red pixels
    red_pixels = find_pixels(input_grid, 2)

    for r, c in red_pixels:
        if r == 0:
            # Create a blue pixel to the left of the red pixel on the top row
            if c - 1 >= 0:
                output_grid[r, c - 1] = 1
        else:
            # Create a 3x3 blue square with the red pixel at the center of the top edge
            for i in range(r -1, r + 2):
                for j in range(c - 1, c + 2):
                    if 0 <= i < height and 0 <= j < width:
                        output_grid[i, j] = 1
            output_grid[r,c] = 2 # Ensure the red pixel remains red

    return output_grid
```
