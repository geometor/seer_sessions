```python
"""
Iterate through each row of the input grid. Within each row, identify the non-zero digits, maintaining their original order. Place these non-zero digits, in their original order, at the bottom of the output grid, starting from the last row and filling upwards, left to right.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by stacking non-zero digits at the bottom, row-wise, preserving within-row order.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    current_row = rows - 1
    current_col = 0

    # Iterate through each row of the input grid
    for r in range(rows):
        # Collect non-zero digits from the current row, preserving order
        non_zero_digits = [val for val in input_grid[r, :] if val != 0]

        # Place the non-zero digits at the bottom of the output grid
        for digit in non_zero_digits:
            if current_col >= cols:  # Move to the next row up if the current row is full
                current_row -= 1
                current_col = 0
            if current_row < 0: #handles edge case where there more non zero pixels than available cells
                break

            output_grid[current_row, current_col] = digit
            current_col += 1

    return output_grid
```
