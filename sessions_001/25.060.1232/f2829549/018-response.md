# f2829549 • 018 • refine_coder

---
```python
"""
The transformation identifies all blue pixels (value '1') in the input grid. For each blue pixel:

1. A corresponding green pixel (value '3') is created in the output grid.
2. The output grid always has 3 columns and the same number of rows as the input grid. All non-green pixels are white (0).
3. The row of the green pixel in the output grid matches the row of the blue pixel in the input grid.
4. The column of the green pixel is determined by the row index of the blue pixel:
   - If the row index is even, the green pixel is placed in column 0.
   - If the row index is odd, the green pixel is placed in column 2.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same number of rows as the input and 3 columns, filled with 0 (white).
    rows = input_grid.shape[0]
    output_grid = np.zeros((rows, 3), dtype=int)

    # Iterate through the input grid to find all blue pixels (value 1).
    for i in range(rows):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 1:
                # If a blue pixel is found, determine the output column based on row index parity.
                output_col = 0 if i % 2 == 0 else 2
                # Set the corresponding pixel in the output grid to green (value 3).
                output_grid[i, output_col] = 3

    return output_grid
```
