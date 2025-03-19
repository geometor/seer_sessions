# 0520fde7 • 014 • example_3 • investigate_coder

---
```python
"""
Transforms an input grid based on the location of a vertical gray stripe and adjacent blue pixels.

1.  **Identify the gray stripe:** Locate the single vertical stripe of gray (5) pixels in the input grid. Note its column index.
2.  **Find adjacent blue pixels**: Find blue pixels that are on the left and on the right of the gray stripe.
3.  **Create output grid**: Create an output grid with dimensions 3x3, initially filled with white (0) pixels.
4.  **Transform to red**: Change the color of cells in the output grid based on the blue pixels next to the grey stripe.
    *   The row number remains the same
    *   The column number is relative to the blue pixel, so it should be the index / 2.
    *   If there is not blue pixel on the left, that is input row 1, then it should be the first column.
"""

import numpy as np

def find_gray_stripe_column(grid):
    """Finds the column index of the vertical gray stripe."""
    for col in range(grid.shape[1]):
        if all(grid[:, col] == 5):
            return col
    return -1  # Should not happen based on problem description

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    # Initialize output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the gray stripe
    gray_stripe_col = find_gray_stripe_column(input_grid)

    # Process each row
    for row in range(input_grid.shape[0]):
        # Find blue pixels to the left and right of the gray stripe
        
        if gray_stripe_col > 0 and input_grid[row, gray_stripe_col - 1] == 1 :
            output_grid[row, (gray_stripe_col - 1) // 2 ] = 2

        if gray_stripe_col < input_grid.shape[1] - 1 and input_grid[row, gray_stripe_col + 1] == 1:
           output_grid[row,( gray_stripe_col + 1) // 2] = 2
           
    return output_grid
```
