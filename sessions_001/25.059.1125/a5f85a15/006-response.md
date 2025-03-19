# a5f85a15 • 006 • refine_coder

---
```python
"""
Locate diagonal lines (top-left to bottom-right and top-right to bottom-left) consisting of a single color.
If a diagonal consists of only a single, non-zero color, change every other pixel to yellow (4), starting from the second pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by modifying single-color diagonals.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    def process_diagonal(row_start, col_start, row_dir, col_dir):
        row, col = row_start, col_start
        diagonal_pixels = []
        while 0 <= row < rows and 0 <= col < cols:
            diagonal_pixels.append((row, col, input_grid[row, col]))
            row += row_dir
            col += col_dir

        # Check if the diagonal consists of a single non-zero color
        non_zero_colors = set(color for _, _, color in diagonal_pixels if color != 0)
        if len(non_zero_colors) == 1:
            skip = True  # Start by skipping
            for r, c, color in diagonal_pixels:
                if color != 0:
                  if not skip:
                      output_grid[r, c] = 4
                  skip = not skip # toggle the skip

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
