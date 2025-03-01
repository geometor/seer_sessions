# cdecee7f • 010 • refine_coder

---
```python
"""
1.  **Selection:** Identify all non-zero (non-white) pixels within the input grid.
2.  **Ordering:** Sort the selected pixels first by their row index in ascending order, and then by their column index, also in ascending order.
3.  **Arrangement:** Create a 3x3 output grid. Populate this grid row by row. For each row in the output grid, select up to the first three pixels from the ordered list of pixels. Place each pixel into the output row, moving from left to right (increasing column index). Once a row is full (3 pixels) or no more pixels are available from this original row index, move to the next row in the output grid. Repeat until the output grid is full (3x3) or there are no more selected pixels to place.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Finds and returns the coordinates and values of non-zero pixels in a grid.
    """
    pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value != 0:
                pixels.append(((row_idx, col_idx), value))
    return pixels

def transform(input_grid):
    """
    Transforms the input grid into a 3x3 output grid by selecting non-zero
    pixels, ordering them by row and then column, and arranging in a 3x3 grid.
    """
    # 1. Selection: Get all non-zero pixels.
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # 2. Ordering: Sort pixels by their original row index, then column index.
    sorted_pixels = sorted(nonzero_pixels, key=lambda item: (item[0][0], item[0][1]))

    # 3. Arrangement: Place into the output grid.
    output_grid = np.zeros((3, 3), dtype=int)
    
    # build output row by row
    output_row = 0
    output_col = 0
    pixel_index = 0

    while output_row < 3 and pixel_index < len(sorted_pixels):
      output_col = 0
      while output_col < 3 and pixel_index < len(sorted_pixels):
        output_grid[output_row, output_col] = sorted_pixels[pixel_index][1]
        pixel_index += 1
        output_col += 1
      output_row += 1

    return output_grid
```
