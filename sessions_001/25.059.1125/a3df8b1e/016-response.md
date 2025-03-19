# a3df8b1e • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule is to replace a single blue pixel in the input grid with a white pixel,
and then create a diagonal line of blue pixels running from the top-right to the bottom-left corner of the grid,
essentially inverting rows and columns.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing a blue pixel and drawing a diagonal line.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the location of the blue pixel (value 1).  Assume there is only one or none.
    blue_pixel_positions = np.where(input_grid == 1)
    if len(blue_pixel_positions[0]) > 0:  # Check if a blue pixel exists
        blue_row, blue_col = blue_pixel_positions[0][0], blue_pixel_positions[1][0]
        output_grid[blue_row, blue_col] = 0  # Replace the blue pixel with white.
    else:  # if no blue pixel found, assume top-right
      blue_row, blue_col = 0, cols-1

    # Create the diagonal of blue pixels
    for r in range(rows):
        for c in range(cols):
            if r == rows - 1 - c :
              output_grid[r,c] = 1

    return output_grid
```
