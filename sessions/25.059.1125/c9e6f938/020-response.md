# c9e6f938 • 020 • refine_coder

---
```python
"""
1.  **Find Orange Pixel:** Locate the orange pixel (value 7) in the input grid. Note its row and column.
2.  **Calculate Extension:** Determine the 'extension amount' using the formula: `extension_amount = input_width - 1 - orange_pixel_column`.
3.  **Create Output Grid:** Create a new, empty output grid.
    *   The width of the output grid is calculated as: `output_width = input_width + (2 * extension_amount)`.
    *  The height is the same as the input.
4.  **Copy Orange Pixel:** Copy the orange pixel from its original position in the input grid to the same position in the output grid.
5.  **Mirror Orange Pixel:**
    *   Place a mirrored orange pixel in the output grid. Its row is 0, and its column is calculated as: `mirrored_column = input_width - 1 + extension_amount`.
6.  **Copy and Extend Remaining Pixels:** For every other pixel in the input grid:
    *    Copy its value to the output grid in the same row and column.
    *    Calculate the extended column: extended_column = input_width - 1 + extension_amount + (original_column - orange_pixel_column)
    *   Place an additional pixel of the same color in the output in row 0 and the extended column.
"""

import numpy as np

def find_orange_pixel(grid):
    # Find the coordinates of the orange pixel (value 7).
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 7:
                return r, c
    return None

def transform(input_grid):
    # Find Orange Pixel
    orange_pixel_coords = find_orange_pixel(input_grid)
    if orange_pixel_coords is None:
      return input_grid # Should not happen, based on problem definition
    original_row, original_col = orange_pixel_coords

    # Calculate Extension
    input_width = input_grid.shape[1]
    extension_amount = input_width - 1 - original_col

    # Create Output Grid
    output_width = input_width + (2 * extension_amount)
    output_height = input_grid.shape[0]
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy Orange Pixel
    output_grid[original_row, original_col] = 7

    # Mirror Orange Pixel
    mirrored_column = input_width - 1 + extension_amount
    output_grid[0, mirrored_column] = 7

    # Copy and Extend Remaining Pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if (r,c) != (original_row, original_col):
                output_grid[r, c] = input_grid[r, c] # copy
                extended_column = input_width - 1 + extension_amount + (c - original_col)
                output_grid[0, extended_column] = input_grid[r,c]



    return output_grid
```
