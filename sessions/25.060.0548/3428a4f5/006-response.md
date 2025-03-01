# 3428a4f5 • 006 • refine_coder

---
```python
"""
1.  **Color Transformation:** Change all pixels of color 2 (red) to color 3 (green).
2.  **Vertical Row Merging:** Combine every two consecutive rows of the grid into a single row. When merging, the color of a pixel in the resulting row is determined as follows:
    *   If the corresponding pixel in the *first* of the two original rows is non-zero, keep that color.
    *   Otherwise, if the corresponding pixel in the *second* of the two original rows is non-zero, use that color.
    *   If both corresponding pixels are zero, the resulting pixel is zero.
3.  If there are an odd number of rows, the final row is kept.
"""

import numpy as np

def change_color(grid, old_color, new_color):
    # Replace all instances of old_color with new_color
    grid[grid == old_color] = new_color
    return grid

def vertical_reduction(grid):
    # Initialize an empty list to hold the new rows
    new_rows = []
    # Iterate through the rows, taking two at a time
    for i in range(0, grid.shape[0], 2):
        # if we're on the last row and its odd, just add to new rows
        if i + 1 == grid.shape[0]:
            new_rows.append(grid[i,:])
        else:
            # Get the two rows
            row1 = grid[i, :]
            row2 = grid[i+1, :]
            # Create new row, taking color from row 1 unless row 2 is not zero
            new_row = np.where(row1 != 0, row1, row2)
            new_rows.append(new_row)

    return np.array(new_rows)


def transform(input_grid):
    # Convert input grid to a NumPy array
    grid = np.array(input_grid)

    # 1. Change color 2 to 3
    grid = change_color(grid, 2, 3)

    # 2. Vertical reduction
    output_grid = vertical_reduction(grid)

    return output_grid.tolist()
```
