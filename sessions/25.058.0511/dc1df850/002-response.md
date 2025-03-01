# dc1df850 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is:
1. Identify all red (2) and magenta (6) pixels in the input grid. Their positions and colors are preserved in the output.
2. Flood Fill: for the top 3 project rows and all columns, perform the steps:
    1. change all white (0) pixels to blue (1).
    2. If a pixel is red, it will retain the color red.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    # Iterate through each cell in the top 3 rows
    for r in range(min(3, rows)):  # Ensure we don't go beyond grid bounds
      for c in range(cols):
        # change white pixels to blue
        if output_grid[r, c] == 0:
          output_grid[r, c] = 1

    return output_grid
```
