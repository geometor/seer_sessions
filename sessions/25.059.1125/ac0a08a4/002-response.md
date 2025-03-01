# ac0a08a4 • 002 • example_3 • investigate_coder

---
```python
"""
Expands each non-zero pixel in the input 3x3 grid into a 3x3 block of the same color in the output grid. The output grid's dimensions are determined by multiplying the number of rows of colored pixels by 3 and the number of columns of colored pixels by 3.
"""

import numpy as np

def get_colored_pixels(grid):
    """
    get a dictionary indexed by (row, col) of colored pixels
    """
    colored_pixels = {}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != 0:
                colored_pixels[(r,c)] = grid[r][c]

    return colored_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    colored_pixels = get_colored_pixels(input_grid)

    # compute rows
    rows = set()
    cols = set()
    for k in colored_pixels.keys():
      rows.add(k[0])
      cols.add(k[1])

    # initialize output_grid
    output_height = len(rows) * 3
    output_width = len(cols) * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for (r, c), color in colored_pixels.items():
        row_start = rows.index(r)*3
        col_start = cols.index(c)*3

        output_grid[row_start:row_start+3, col_start:col_start+3] = color

    return output_grid.tolist()
```
