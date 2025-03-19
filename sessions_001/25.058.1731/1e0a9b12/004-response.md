# 1e0a9b12 • 004 • refine_coder

---
```python
"""
The transformation rule involves rearranging non-zero pixels from the input grid to the output grid.
Pixels are moved to the bottom-most available row, filling the output grid column-wise from left to right.
The order of pixels is determined by reading the input grid row by row from top to bottom, and within each row, from left to right.
Empty rows at the top of the output grid are removed.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving all non-zero pixels to the bottom,
    filling columns from left to right, and maintaining the order of appearance 
    in the input (reading row-wise, then column-wise).
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Extract non-zero pixels in their order of appearance
    non_zero_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append(input_grid[r, c])

    # 2. Determine the dimensions of the output grid.
    num_non_zero = len(non_zero_pixels)
    if num_non_zero == 0:
        return []  # Return empty grid if no non-zero pixels

    output_rows = (num_non_zero + cols - 1) // cols  # Calculate the required number of rows
    output_grid = np.zeros((output_rows, cols), dtype=int)


    # 3. Fill the output grid column-wise
    pixel_index = 0
    for c in range(cols):
        for r in range(output_rows):
            if pixel_index < num_non_zero:
                output_grid[r, c] = non_zero_pixels[pixel_index]
                pixel_index += 1

    return output_grid.tolist()
```
