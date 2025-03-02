# 239be575 • 034 • refine_coder

---
```python
"""
The transformation rule identifies the horizontal distance between the red pixel (value 2) and the nearest edge of the grid or an azure pixel (value 8). The output is a 1x1 grid containing this distance multiplied by 2.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid based on the described rule.
    """
    input_grid = np.array(input_grid)

    # Find the row containing the red pixel (2).
    red_row_index = -1
    red_col_index = -1
    for i, row in enumerate(input_grid):
        if 2 in row:
            red_row_index = i
            red_col_index = np.where(row == 2)[0][0]
            break

    # If no red pixel is found, return 0.
    if red_row_index == -1:
        return np.array([[0]])

    red_row = input_grid[red_row_index]

    # Calculate distance to the left edge or azure pixel.
    left_distance = red_col_index
    for i in range(red_col_index - 1, -1, -1):
        if red_row[i] == 8:
            left_distance = red_col_index - i -1
            break

    # calculate distance to the right edge or azure pixel
    right_distance = len(red_row) - red_col_index - 1
    for i in range(red_col_index + 1, len(red_row)):
      if red_row[i] == 8:
        right_distance = i - red_col_index - 1
        break
        
    # min distance
    distance = min(left_distance, right_distance)

    # The output is the distance multiplied by 2.
    output_value = distance * 2
    output_grid = np.array([[output_value]])

    return output_grid
```
