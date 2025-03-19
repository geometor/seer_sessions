# c444b776 • 008 • example_1 • investigate_coder

---
```python
"""
1.  **Identify the Axis:** Locate the vertical line of yellow (4) pixels that runs down the center of the grid. This is the reflection axis and its position and color do not change. The horizontal yellow line does change.
2.  **Reflect Other Pixels:** For every non-yellow pixel in the input grid to the left or right of the central yellow line, find its corresponding position on the *opposite* side of the vertical axis (the vertical yellow line). If the non-yellow input pixel is N pixels away for the central line, then copy this pixel to N pixels away on the other side.
3. The output of the process maintains the original central line.
"""

import numpy as np

def find_vertical_yellow_line(grid):
    # Find the column index of the vertical yellow line.
    rows, cols = grid.shape
    for j in range(cols):
        if all(grid[:, j] == 4):
            return j
    return -1  # Should not happen in valid input

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # find center line
    center_col = find_vertical_yellow_line(input_grid)

    # reflect non yellow cells across
    for i in range(rows):
        for j in range(cols):
            if j != center_col and input_grid[i,j] != 4:
                distance = center_col - j
                new_col = center_col + distance
                if 0 <= new_col < cols:
                    output_grid[i, new_col] = input_grid[i, j]

    return output_grid
```
