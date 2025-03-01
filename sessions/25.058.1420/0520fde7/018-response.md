# 0520fde7 • 018 • refine_coder

---
```python
"""
1. Examine each row of the input grid.
2. Count the blue pixels in each row.
3. Create an output grid of size 3x3.
4. For each row in the input, if the count of blue pixels is greater than zero, place a red pixel in the output grid.
    - The red pixel's row will match the input row.
    - The red pixel's x-coordinate will be one less than the number of blue pixels counted.
5. If a row contains zero blue pixels, no red pixel is placed for that row.
6. If all rows contain zero blue pixels, the output grid remains unchanged (all white/zero).
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid with all white (0) pixels.
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through each row of the input grid.
    for i, row in enumerate(input_grid):
        # Count the number of blue (1) pixels in the current row.
        blue_count = np.count_nonzero(row == 1)

        # If the count of blue pixels is greater than 0, place a red (2) pixel
        # in the output grid at the corresponding row and x-coordinate = blue_count - 1.
        if blue_count > 0:
            output_grid[i, blue_count - 1] = 2

    return output_grid
```

