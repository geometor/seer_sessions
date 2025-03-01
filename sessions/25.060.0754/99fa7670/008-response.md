# 99fa7670 • 008 • refine_coder

---
```python
"""
1.  **Identify Non-White Pixels:** Find all pixels in the input grid that are not white (value 0).
2.  **Vertical Column Transformation:** For each non-white pixel, identify its color and its column.
3. **Fill Column**: Fill the entire column with the color of the identified pixel, from the top row (row 0) to the bottom row of the grid. The filled section replaces all values in the output grid.

In short, the algorithm finds the non-white pixels and extends their color vertically downwards to the bottom of the grid, creating a column, overwriting any color or white space in that column.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by filling columns based on non-white pixels.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell to find non-white pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                color = input_grid[r, c]
                # Fill the entire column with the color
                output_grid[:, c] = color
    return output_grid
```
