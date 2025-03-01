# 05269061 • 012 • refine_coder

---
```python
"""
The output grid has the same dimensions as the input grid and uses the same set of colors, including 0. The transformation applies a pattern based on the cell's row and column indices, cycling through the sorted non-zero input colors. The pattern is determined by (row + col) % 3.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as input_grid.
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get the distinct non-zero colors from the input grid, sorted.
    distinct_colors = sorted(list({val for row in input_grid for val in row if val != 0}))

    # Apply the pattern based on (row + col) % 3.
    for i in range(rows):
        for j in range(cols):
            if (i + j) % 3 == 0:
                # Use the second non-zero color (index 1). Handle cases where there may be fewer distinct colors.
                output_grid[i, j] = distinct_colors[1 % len(distinct_colors)]
            elif (i + j) % 3 == 1:
                # Use the third non-zero color (index 2 if exists, otherwise wrap around).
                output_grid[i, j] = distinct_colors[2 % len(distinct_colors)]
            elif (i + j) % 3 == 2:
                # Use the first non-zero color.
                output_grid[i, j] = distinct_colors[0 % len(distinct_colors)]


    return output_grid
```
