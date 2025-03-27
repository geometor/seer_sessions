```python
"""
Iterate through the input grid column by column, and within each column, row by row.
Identify non-zero pixels. For each non-zero pixel, record its value and original column index.
Create an output grid of the same dimensions as the input grid, filled with zeros.
Iterate through the recorded non-zero pixels. For each pixel:
    Find the lowest available row in the output grid *within the pixel's original column*.
    Place the pixel's value in that cell.
Return the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by stacking non-zero digits at the bottom, preserving column order.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through columns
    for c in range(cols):
        # Iterate through rows within each column, from bottom to top
        available_row = rows - 1
        for r in range(rows):
            if input_grid[r, c] != 0:
                # Place the non-zero pixel in the lowest available row of the same column
                output_grid[available_row, c] = input_grid[r, c]
                available_row -= 1  # Move the available row up for the next non-zero pixel in this column

    return output_grid
```
