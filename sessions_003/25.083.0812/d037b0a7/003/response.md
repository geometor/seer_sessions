```python
"""
1.  **Identify Seed Pixels:** Examine the top row (row 0) and the leftmost column (column 0) of the input grid. The non-zero pixels on these edges are the "seed" pixels.

2.  **Column Propagation:** For each non-zero pixel in the top row, change all pixels in its column to match the color of that top-row pixel.

3.  **Row Propagation, with Override:** For each non-zero pixel in the left column, iterate through its row. *However*, only change the color of a cell in that row if it hasn't *already* been changed during the column propagation step. In other words, column propagation takes precedence.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])

    # Keep track of changed cells
    changed_cells = set()

    # Column Propagation
    for j in range(width):
        if input_grid[0][j] != 0:
            for i in range(height):
                output_grid[i][j] = input_grid[0][j]
                changed_cells.add((i, j))

    # Row Propagation, with Override
    for i in range(height):
        if input_grid[i][0] != 0:
            for j in range(width):
                if (i, j) not in changed_cells:
                    output_grid[i][j] = input_grid[i][0]

    return output_grid
```
