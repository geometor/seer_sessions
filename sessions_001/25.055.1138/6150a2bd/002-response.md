# 6150a2bd • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is a 90-degree counter-clockwise rotation of the input grid. The color values of the pixels are rotated, but the center pixel remains unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  We'll modify it in place.
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Rotate the grid counter-clockwise by 90 degrees.
    for i in range(rows):
      for j in range(cols):
        output_grid[cols - 1 - j][i] = input_grid[i][j]

    return output_grid
```
