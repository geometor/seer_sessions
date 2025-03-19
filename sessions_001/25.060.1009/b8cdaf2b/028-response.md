# b8cdaf2b • 028 • refine_coder

---
```python
"""
1.  **Copy Input:** Create a copy of the input grid to serve as the output grid.
2.  **Find Yellow:** Locate all yellow pixels within the input grid.
3.  **Group by Column:** Group the identified yellow pixels according to their column indices.
4.  **Calculate Target Rows:** For each column that contains one or more yellow pixels:
    *   Determine the *minimum* row index (`min_row`) among the yellow pixels in that column.
    *   Calculate two target row indices:
        *   `target_row_1 = min_row - 3`
        *   `target_row_2 = min_row - 2`
5.  **Place Yellow Pixels:** For each column with yellow pixels:
    *   If `target_row_1` is within the grid's boundaries (0 to height-1, inclusive), place a yellow pixel at the position (`target_row_1`, current column) in the output grid.
    *   If `target_row_2` is within the grid's boundaries (0 to height-1, inclusive), place a yellow pixel at the position (`target_row_2`, current column) in the output grid.
6.  **Unchanged Pixels:** All other pixels in the output grid remain the same as in the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height = input_grid.shape[0]
    width = input_grid.shape[1]

    # Find all yellow pixels
    yellow_pixels = []
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 4:
                yellow_pixels.append((r, c))

    # Group yellow pixels by column
    yellow_cols = {}
    for r, c in yellow_pixels:
        if c not in yellow_cols:
            yellow_cols[c] = []
        yellow_cols[c].append(r)

    # Determine target rows and place yellow pixels
    for col, rows in yellow_cols.items():
        min_row = min(rows)
        target_row_1 = min_row - 3
        target_row_2 = min_row - 2

        # Check boundaries
        if 0 <= target_row_1 < height:
            output_grid[target_row_1, col] = 4
        if 0 <= target_row_2 < height:
            output_grid[target_row_2, col] = 4

    return output_grid
```

