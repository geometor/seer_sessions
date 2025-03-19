# d406998b • 020 • example_4 • investigate_coder

---
```python
"""
The transformation selectively changes every third gray pixel to green, starting from the right, while leaving all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing every third gray pixel to green, starting from the right.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each row
    for row in range(rows):
        # Find gray pixels in the current row, from right
        gray_pixels = []
        for col in reversed(range(cols)):
          if output_grid[row, col] == 5:
            gray_pixels.append(col)

        # Change every third gray pixel to green
        count = 0
        for col in gray_pixels:
            count += 1
            if count == 1:
                output_grid[row, col] = 3
            if count == 3:
                count = 0 # reset

    return output_grid
```
