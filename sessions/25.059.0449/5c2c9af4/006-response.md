# 5c2c9af4 • 006 • refine_coder

---
```python
"""
The transformation extends azure (color 8) pixels vertically and connects them diagonally. The first azure pixel in the input anchors a vertical line spanning the entire height of the grid. Subsequent azure pixels anchor vertical lines starting from their row index to the bottom of the grid.  All azure pixels are then connected diagonally, creating a continuous azure region.
"""

import numpy as np

def get_azure_pixels(grid):
    """Finds the coordinates of all azure (8) pixels in the grid."""
    return np.argwhere(grid == 8)

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.zeros_like(input_grid)
    output_grid[:] = 0  # Ensure the output grid starts blank.
    azure_pixels = get_azure_pixels(input_grid)

    if len(azure_pixels) == 0:
        return output_grid

    # Vertical Replication - First pixel, full height.  Others, from row down.
    for i, pixel in enumerate(azure_pixels):
        row, col = pixel
        if i == 0:
            output_grid[:, col] = 8
        else:
            output_grid[row:, col] = 8

    # Connect azure pixels diagonally.
    for i in range(len(azure_pixels) - 1):
        row1, col1 = azure_pixels[i]
        row2, col2 = azure_pixels[i + 1]

        row_diff = row2 - row1
        col_diff = col2 - col1

        if col_diff != 0:
          row_step = 1 if row_diff>0 else -1
          col_step = 1 if col_diff>0 else -1

          current_row, current_col = row1, col1
          while (current_col != col2):
            current_row += row_step
            current_col += col_step
            if 0 <= current_row < output_grid.shape[0] and 0 <= current_col < output_grid.shape[1]:
                output_grid[current_row,current_col] = 8

    return output_grid
```
