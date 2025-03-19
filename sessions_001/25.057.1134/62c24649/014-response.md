# 62c24649 • 014 • example_3 • investigate_coder

---
```python
"""
The input grid is embedded in the center of the output grid. The input is then mirrored horizontally and vertically to create a symmetrical pattern.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2, input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # embed input grid into output grid
    output_grid[0:input_rows, 0:input_cols] = input_grid

    # mirror horizontally
    output_grid[0:input_rows, input_cols:output_cols] = np.fliplr(input_grid)

    # mirror vertically
    output_grid[input_rows:output_rows, 0:input_cols] = np.flipud(input_grid[0:input_rows, 0:input_cols])
    output_grid[input_rows:output_rows, input_cols:output_cols] = np.flipud(input_grid[0:input_rows, 0:input_cols])
    output_grid[input_rows:output_rows, input_cols:] = np.fliplr(output_grid[input_rows:output_rows, 0:input_cols])

    return output_grid
```
