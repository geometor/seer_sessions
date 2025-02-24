# 6150a2bd • 002 • example_1 • investigate_coder

---
```python
"""
The input grid is rotated 90 degrees clockwise to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Rotate the grid 90 degrees clockwise
    for i in range(rows):
        for j in range(cols):
            output_grid[j][cols - 1 - i] = input_grid[i][j]

    return output_grid.tolist()
```
