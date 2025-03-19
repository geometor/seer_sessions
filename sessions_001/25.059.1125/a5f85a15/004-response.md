# a5f85a15 • 004 • refine_coder

---
```python
"""
Locate diagonal lines (top-left to bottom-right and top-right to bottom-left) of non-zero pixels.
Traverse each diagonal, skipping the first non-zero pixel, changing the next to yellow (4), 
and repeating this skip-then-change process.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by modifying diagonals.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    def process_diagonal(row_start, col_start, row_dir, col_dir):
        row, col = row_start, col_start
        skip = True  # Start by skipping the first non-zero pixel
        while 0 <= row < rows and 0 <= col < cols:
            if input_grid[row, col] != 0:
                if not skip:
                    output_grid[row, col] = 4
                skip = not skip  # Toggle skip for the next non-zero pixel
            row += row_dir
            col += col_dir

    # Iterate through diagonals from top-left to bottom-right
    for i in range(rows):
        process_diagonal(i, 0, 1, 1)  # Start from first column
    for j in range(1, cols):
        process_diagonal(0, j, 1, 1)  # Start from first row

    # Iterate through diagonals from top-right to bottom-left
    for i in range(rows):
        process_diagonal(i, cols - 1, 1, -1)  # Start from the last column
    for j in range(cols - 1):
        process_diagonal(0, j, 1, -1)

    return output_grid
```
