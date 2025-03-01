# 90f3ed37 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation identifies azure pixels and creates blue pixels to the right in rows, based on white '0' pixels adjacent to the azure pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is an azure pixel (value 8)
            if input_grid[r, c] == 8:
                # Iterate through the cells to the right of the azure pixel in the same row
              for c_right in range(c+1, cols):
                  if input_grid[r,c_right] == 0:
                      output_grid[r,c_right] = 1
                  else:
                      break

    return output_grid
```
