# 6d58a25d • 014 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all red pixels (value '2'), orange pixels (value '7'), and any other non-zero pixels within the input grid.
2.  **Preserve Non-Red Objects:** All non-red pixels (including orange and others like green in Example 5) in the input grid should be present in the output at the exact same position.
3.  **Conditional Red Replication:** For every red pixel in the input, create a vertical column in the output.  The column starts at the row containing the red pixel. Extend the column downwards, one row at a time.
4. **Stopping Conditions:** Stop the downward extension of a red column if *either* of the following conditions is met:
    *   A non-zero pixel (any color other than background) is encountered in the column.
    *   The bottom row of the grid is reached.
5.  **Output Construction:** Place the replicated red pixels, along with the original red pixels, and all other non-zero pixels, into a new grid.  Preserve the background (value '0') where no other objects are present.

In summary: Copy each red pixel downwards, stopping when *any non-zero pixel* or the bottom of the grid is encountered. Preserve the positions of all other non-zero colored pixels.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            # Preserve Non-Red Objects
            if input_grid[r, c] != 0 and input_grid[r,c] != 2:
                output_grid[r, c] = input_grid[r,c]
            # Red Replication
            elif input_grid[r, c] == 2:
                output_grid[r,c] = 2 # preserve original red
                # set current and all lower rows to 2, until non-zero or bottom
                for r_prime in range(r + 1,rows):
                    if input_grid[r_prime,c] != 0:
                        break # stop at any non-zero pixel
                    output_grid[r_prime, c] = 2

    return output_grid
```
