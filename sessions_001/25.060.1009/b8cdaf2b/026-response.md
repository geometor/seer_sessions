# b8cdaf2b • 026 • refine_coder

---
```python
"""
1.  **Find Yellow Pixels:** Identify all pixels in the input grid that are yellow (value 4).

2.  **Determine Target Rows:** For each column that contains one or more yellow pixels, calculate two target row indices:
    *   `target_row_1 = min(yellow_row_indices) - 3`
    *   `target_row_2 = min(yellow_row_indices) - 2`

3.  **Place Yellow Pixels:** If the calculated target row indices are within the grid boundaries place a yellow pixel in each of the identified columns at both target rows.

4. Leave other pixels unchanged.
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
