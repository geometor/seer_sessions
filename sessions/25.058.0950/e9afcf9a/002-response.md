# e9afcf9a • 002 • example_2 • investigate_coder

---
```python
"""
The transformation takes a 2xN grid where the first row is a single color (color_1) and the second row is a different single color (color_2). It creates a new grid of the same dimensions (2xN) and fills it by alternating colors. The alternation in the first row starts with color_1, and the alternation in the second row starts with color_2.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 2xN grid by alternating the colors of the two rows.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)
    color1 = input_grid[0, 0]
    color2 = input_grid[1, 0]

    # Iterate through columns
    for j in range(cols):
        # Alternate colors for each row
        if j % 2 == 0:
            output_grid[0, j] = color1
            output_grid[1, j] = color2
        else:
            output_grid[0, j] = color2
            output_grid[1, j] = color1

    return output_grid
```
