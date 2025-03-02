# d406998b • 014 • refine_coder

---
```python
"""
1.  Iterate through each row of the input grid.
2.  For each row, keep track of the count of gray (5) pixels encountered so far. This is the `gray_order`.
3. Determine if the current row number has odd parity. The first row is 1, and has odd parity.
4.  If the row has odd parity:
    *   If a pixel is gray (5) and the `gray_order` is odd, change the pixel's color to green (3).
5. If the row has even parity:
    * do not change any pixels.
6. All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(rows):
        gray_count = 0  # Reset gray_order for each row
        row_parity = (r + 1) % 2 # determine row parity

        # Iterate through each column of the current row
        for c in range(cols):
            # Check for odd row parity
            if row_parity != 0:
                # Check if the current pixel is gray (5)
                if input_grid[r, c] == 5:
                    gray_count += 1  # Increment gray_order
                    # change gray to green if gray_order is odd
                    if gray_count % 2 != 0:
                        output_grid[r, c] = 3  # change gray to green
            # Even row parity - do not change
            else:
                continue # do nothing

    return output_grid
```
