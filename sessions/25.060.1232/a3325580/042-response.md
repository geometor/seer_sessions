# a3325580 • 042 • refine_coder

---
```python
"""
1. Identify Unique Colors: Examine the input grid to determine the unique, non-zero colors present.
2. Determine Output Row Vector: create an output which is a single row
3. Count unique colors. Determine the number of unique colors in input.
4. Create output. Create a row vector grid. If there is only one unique color, the output is a 1x1 grid with that color. If there are more than one unique colors, output is a 1 x *n* grid, where n is the number of unique colors.
"""

import numpy as np

def get_unique_colors(grid):
    # get the unique colors in the input grid, excluding 0
    return np.unique(grid[grid != 0])

def transform(input_grid):
    # get unique colors, excluding white (0)
    unique_colors = get_unique_colors(input_grid)
    num_colors = len(unique_colors)

    # create output grid: 1 row, columns = number of unique colors
    if num_colors == 1:
        output_grid = np.zeros((1, 1), dtype=int)
        output_grid[0,0] = unique_colors[0]
    else:
        output_grid = np.zeros((1, num_colors), dtype=int)
        # fill in the output grid in row major order
        for index, val in enumerate(unique_colors):
            output_grid[0, index] = val
    return output_grid
```
