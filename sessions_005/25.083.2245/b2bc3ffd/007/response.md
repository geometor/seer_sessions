```python
"""
Transforms an input grid by moving non-orange (7) and non-azure (8) pixels
upwards within their columns as much as possible, maintaining their relative
order. The remaining empty spaces (except the bottom row) are then filled with
orange (7) pixels. The bottom row, filled with azure (8), remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    bottom_row = rows - 1

    # 1. Iterate through each column
    for c in range(cols):
        # 2. Identify Mobile Pixels in the current column (above the bottom row)
        mobile_pixels = []
        for r in range(rows - 1):  # Exclude the bottom row
            if output_grid[r, c] != 7 and output_grid[r, c] != 8:
                mobile_pixels.append((r, output_grid[r, c]))

        # 3. Clear the column above the bottom row (replace with 7, orange)
        for r in range(rows - 1):
            if output_grid[r,c] != 8: # safety check
                output_grid[r, c] = 7

        # 4. Place Mobile Pixels back into the column, maintaining order
        new_row = 0
        for _, color in mobile_pixels:
            while new_row < bottom_row and output_grid[new_row, c] != 7:
                new_row += 1
            if new_row < bottom_row: # safety check
                output_grid[new_row, c] = color
                new_row += 1

    return output_grid
```