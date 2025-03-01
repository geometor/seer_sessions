# 539a4f51 • 012 • example_2 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Expand the grid: Double the width and height of the input grid.
2. Replicate Input Pattern: Copy the values in the input grid (except '0's) to the top-left quadrant of the expanded output grid.
3. Fill with '1': Fill all remaining cells in the output with the value '1' (blue).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.ones((output_height, output_width), dtype=int)

    # change output pixels
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] != 0:
              output_grid[row, col] = input_grid[row, col]

    return output_grid
```
