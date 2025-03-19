# f5b8619d • 006 • refine_coder

---
```python
"""
The input grid expands to an output grid where the width is three times the input width, and the height is two times the input height plus one.
Two new colors, white (0) and azure (8), are introduced.
The output follows a repeating pattern based on the input rows. The pattern for each set of three output rows is:
  1. The first row: Input pixel, 0, 8, repeated for all pixels in the input row.
  2. The second row: All 0s.
  3. The third row: 8, 0, 8, 8, 0, 8, 8, 0, 8.
This pattern is repeated for each input row.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2 + 1, input_cols * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Change output pixels according to the described pattern
    for i in range(input_rows):
        # First row of the pattern
        for j in range(input_cols):
            output_grid[i * 2, j * 3] = input_grid[i, j]
            output_grid[i * 2, j * 3 + 1] = 0
            output_grid[i * 2, j * 3 + 2] = 8

        # Second row of the pattern
        output_grid[i * 2 + 1, :] = 0

        # Third row of the pattern
        if i*2+2 < output_rows: # making sure not to exceed boundaries
            output_grid[i*2 + 2, 0] = 8
            output_grid[i*2 + 2, 1] = 0
            output_grid[i*2 + 2, 2] = 8
            output_grid[i*2 + 2, 3] = 8
            output_grid[i*2 + 2, 4] = 0
            output_grid[i*2 + 2, 5] = 8
            output_grid[i*2 + 2, 6] = 8
            output_grid[i*2 + 2, 7] = 0
            output_grid[i*2 + 2, 8] = 8
    return output_grid
```
