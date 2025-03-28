# feca6190 • 012 • refine_coder

---
```python
"""
1.  **Find the Non-Zero Pixel:** Examine the input grid to identify the single pixel with a non-zero value (representing a color other than white). Note its color and its position (row and column indices).

2.  **Determine Output Grid Size:** Create an output grid whose both dimensions are equal to the length of the diagonal. This length should be determined by getting the maximum dimension from input.

3.  **Create the Diagonal:** In the output grid, create a diagonal line of pixels.
    *   If the input contains only 1 row, then the diagonal starts from the bottom-left corner, and moving one step up and one step right for each subsequent pixel on this diagonal.
    *   Otherwise, The diagonal goes from the top-right.
    *   The length of the diagonal will be equal to the largest dimension from the input.
    *   All pixels on the diagonal should have the same color as the non-zero pixel found in the input grid.

4.  **Fill Remaining Pixels:** Set all pixels in the output grid that are *not* part of the diagonal to white (0).
"""

import numpy as np

def find_nonzero_pixel(grid):
    """Finds the (first) non-zero pixel in a grid."""
    non_zero_indices = np.where(grid != 0)
    if non_zero_indices[0].size > 0:
        row = non_zero_indices[0][0]
        col = non_zero_indices[1][0]
        value = grid[row, col]
        return row, col, value
    return None, None, 0 # Return 0 for value if no non-zero pixel is found

def transform(input_grid):
    # Find the non-zero pixel.
    row, col, value = find_nonzero_pixel(input_grid)

    # Determine output grid size.
    input_rows, input_cols = input_grid.shape
    output_size = max(input_rows, input_cols)
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Create the diagonal.
    if input_rows == 1:
        for i in range(output_size):
            output_grid[output_size - 1 - i, i] = value
    else:
        for i in range(output_size):
          output_grid[i, output_size-1-i] = value
    return output_grid
```
