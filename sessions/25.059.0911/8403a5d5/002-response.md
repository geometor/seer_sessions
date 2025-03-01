# 8403a5d5 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1.  **Identify the non-zero pixel:** Locate the single pixel in the input grid that has a color other than '0' (white). Note its color and x-coordinate (column).
2.  **Create repeating column:** For every row in the output grid. at the x-coordinate of the identified, non-zero pixel. fill the cell with the original color.
3. **Create alternating grey Columns:** Fill every other cell in the output, with the same x-coordinate relative to the original color, with '5' (gray)
4. **Create empty Columns:** Fill every other remaining column with the original color, starting with an offset.
5.  **Fill Remaining:** Fill the rest of the pixels with '0' (white).
"""

import numpy as np

def find_non_zero_pixel(grid):
    # Find the coordinates and value of the non-zero pixel
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] != 0:
                return x, y, grid[y, x]
    return None, None, None

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""

    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Find the non-zero pixel in the input grid
    x_original, _, color_original = find_non_zero_pixel(input_grid)

    if x_original is None:  # Handle cases with no non-zero pixel.
        return output_grid


    # Create the repeating pattern in the output grid
    for row in range(rows):
      for col in range(cols):
        if col == x_original:
          output_grid[row,col] = color_original
        elif (col - x_original) % 2 == 0:
          output_grid[row,col] = color_original
        elif (col-x_original) % 2 != 0:
          if col % 2 == x_original % 2:
            output_grid[row,col] = 5


    return output_grid
```
