# 3428a4f5 • 008 • refine_coder

---
```python
"""
1.  **Color Transformation:** Change all pixels of color 2 (red) to color 3 (green).
2.  **Vertical Row Merging:** Combine every two consecutive rows of the grid into a single row.
    *   Iterate through the rows of the input grid, taking two at a time (row `i` and row `i+1`).
    *   For each column index `j`:
        *   If both `input[i][j]` and `input[i+1][j]` are non-zero:
           *   If the new row has space, put the two non-zero values adjacent, using 3
        *   Else If `input[i][j]` is non-zero, `output[k][j]` = `input[i][j]`
        *   Else If `input[i+1][j]` is non-zero, `output[k][j]` = `input[i+1][j]`
        *   Otherwise (both are zero), `output[k][j] = 0`
    *   If the input grid has an odd number of rows, the last row is appended to the output without merging.
3. If there are more than 1 non-zero values in a column after the red-green color change, keep *both* in the merged row.
"""

import numpy as np

def change_color(grid, old_color, new_color):
    # Replace all instances of old_color with new_color
    grid[grid == old_color] = new_color
    return grid

def vertical_reduction(grid):
    new_rows = []
    for i in range(0, grid.shape[0], 2):
        if i + 1 == grid.shape[0]:
            new_rows.append(grid[i,:])
        else:
            row1 = grid[i, :]
            row2 = grid[i+1, :]
            new_row = np.zeros_like(row1)
            insert_index = 0
            for j in range(row1.shape[0]):
                if row1[j] != 0 and row2[j] != 0:
                    if insert_index < new_row.shape[0]:
                        new_row[insert_index] = row1[j]
                        insert_index += 1
                    if insert_index < new_row.shape[0]:
                        new_row[insert_index] = row2[j]
                        insert_index += 1

                elif row1[j] != 0:
                    if insert_index < new_row.shape[0]:
                        new_row[insert_index] = row1[j]
                        insert_index += 1
                elif row2[j] != 0:
                   if insert_index < new_row.shape[0]:
                        new_row[insert_index] = row2[j]
                        insert_index += 1

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
