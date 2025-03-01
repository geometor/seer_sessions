# 56ff96f3 • 028 • refine_coder

---
```python
"""
1.  **Identify Orange Pixels:** Locate all pixels with the color orange in the input grid.
2.  **Find Topmost and Bottommost Rows:** Among the orange pixels, find the row index of the topmost orange pixel and the bottommost orange pixel.
3.  **Determine Output Region:** Calculate the top row of the output rectangle by subtracting 2 from the topmost orange pixel's row index. If this value goes beyond grid limits, start from 0. The bottom row of the output region is the bottommost row of the orange pixels.
4. **Determine min and max columns** The first and last column of the rectangle should match those of the orange pixels.
5.  **Fill Rectangle:** Create an output grid of the same size as the input. Fill the calculated rectangle within the output grid with orange pixels.
"""

import numpy as np

def find_orange_pixels(grid):
    # Find coordinates of all orange pixels (value 7).
    orange_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 7:
                orange_pixels.append((row_index, col_index))
    return orange_pixels

def find_topmost_row(pixels):
    # Find the minimum row index among a set of pixels.
    if not pixels:
        return None
    min_row = pixels[0][0]
    for row, _ in pixels:
        min_row = min(min_row, row)
    return min_row

def find_bottommost_row(pixels):
    # Find the maximum row index among set of pixels.
    if not pixels:
      return None
    max_row = pixels[0][0]
    for row, _ in pixels:
      max_row = max(max_row, row)
    return max_row

def transform(input_grid):
    # Initialize output grid with the same dimensions and default white pixels.
    output_grid = np.zeros_like(input_grid)

    # Find all orange pixels.
    orange_pixels = find_orange_pixels(input_grid)

    if not orange_pixels:
        return output_grid

    # Determine the topmost and bottommost row of the orange pixels.
    topmost_row = find_topmost_row(orange_pixels)
    bottommost_row = find_bottommost_row(orange_pixels)

    # Calculate the row two rows above the topmost orange pixel.
    start_row = max(0, topmost_row - 2)

    # Find min and max columns
    min_col = min(col for _, col in orange_pixels)
    max_col = max(col for _, col in orange_pixels)
    

    # Fill the rectangle with orange.
    for row in range(start_row, bottommost_row + 1):
        for col in range(min_col, max_col + 1):
            output_grid[row, col] = 7

    return output_grid
```
