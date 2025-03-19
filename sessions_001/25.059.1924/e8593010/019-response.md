# e8593010 • 019 • refine_coder

---
```python
"""
1. Preserve Gray: If a pixel is gray, its color remains unchanged.
2. Transform White: If a pixel is white, its new color depends on its row and column indices:
    *   If the row index is even:
        *   If the column index is also even, the color changes to red (2).
        *    If the column index is odd, change color to blue (1).
    *    If the row index is odd:
        *   If the column index is even:
            *   If floor((row index - 1) / 2) is even, change color to blue(1)
            *   If floor((row index - 1) / 2) is odd, change color to green(3).
        *    If the column index is odd:
            *    If floor(row index / 2) is even, the color changes to green (3).
            *    If floor(row index / 2) is odd, change color to blue (1).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 0:  # White pixel
                if r % 2 == 0:  # Even row
                    if c % 2 == 0:  # Even column
                        output_grid[r][c] = 2  # Red
                    else:  # Odd column
                        output_grid[r][c] = 1  # Blue
                else:  # Odd row
                    if c % 2 == 0:  # Even column
                        if ((r - 1) // 2) % 2 == 0:
                            output_grid[r][c] = 1 # Blue
                        else:
                            output_grid[r][c] = 3 # Green
                    else:  # Odd column
                        if  (r // 2) % 2 == 0:
                            output_grid[r][c] = 3  # Green
                        else:
                            output_grid[r][c] = 1  # Blue
    return output_grid
```
