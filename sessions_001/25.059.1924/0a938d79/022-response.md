# 0a938d79 • 022 • example_4 • investigate_coder

---
```python
"""
1.  **Identify Key Rows:** Find the rows in the input grid that contains non-zero values.
2.  **Replicate Rows:** Copy that row, that is, expand to fill the same color value in the full row.
3.  **Copy Pattern:** Copy the pattern of filled rows and repeat.
"""

import numpy as np

def get_colored_rows(grid):
    colored_rows = []
    for i, row in enumerate(grid):
        if np.any(row != 0):
            colored_rows.append((i,row))
    return colored_rows

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # get colored rows
    colored_rows = get_colored_rows(input_grid)

    # replicate rows
    row_idx = 0
    for i in range(len(colored_rows)):
        row_num, color_row = colored_rows[i]
        full_color_row = np.full(input_grid.shape[1], color_row[np.where(color_row !=0)[0][0]])
        output_grid[row_idx] = full_color_row
        row_idx += 1

    # copy pattern
    pattern = output_grid[:row_idx]
    num_repeats = len(output_grid) // len(pattern)
    output_grid = np.tile(pattern,(num_repeats,1))

    return output_grid.tolist()
```
