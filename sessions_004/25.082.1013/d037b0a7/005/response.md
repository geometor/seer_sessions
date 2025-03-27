```python
"""
1.  **Identify Non-Zero Pixels:**  Locate all pixels in the input grid that have a value other than 0.

2.  **Conditional Horizontal Propagation (Leftward):**
    *   For each non-zero pixel, examine the pixels to its *left* in the same row.
    *   If a pixel to the left has a value of 0, change that pixel's value to match the non-zero pixel.
    *   Stop this leftward propagation when either the left edge of the grid is reached or a non-zero pixel is encountered.

3.  **Conditional Vertical Propagation (Downward):**
    *  For each pixel in the *output* grid:
    * If a pixel is not zero valued, fill down with that value until the end of the column.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Conditional Horizontal Propagation (Leftward)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                #fill left
                for k in range(c - 1, -1, -1):
                    if output_grid[r, k] == 0:
                        output_grid[r, k] = input_grid[r, c]
                    else:
                        break  # Stop at non-zero pixel

    # Conditional Vertical Propagation (Downward)
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] != 0:  # check output grid
                #fill values down
                for k in range(r + 1, rows):
                    output_grid[k, c] = output_grid[r, c]

    return output_grid
```
