```python
"""
1.  **Initialization:** Create an output grid of the same dimensions as the input grid, filled initially with zeros.

2.  **Bottom-Left Start:** Set the bottom-left pixel of the output grid to blue (1).

3.  **Iterative Pattern Filling:** Iterate through the output grid row by row, from bottom to top (rows) and left to right (columns):

    *   If it is the bottom-left pixel, skip (already set).

    *   If in the first row from the bottom: place alternating 1 and 8. Starting with 1 in the first position, then place an 8 in the next position, continuing to alternate.

    *   Otherwise (for rows above the bottom row):

        *   Consider the pixel directly below the current position, call this y.
        *   If y is 1 then place 8.
        *   If y is 8 then:
            * Consider the pixel to the left and one row down, call this x.
            * If x is 1: place 1.
            * if x is 8: place 8.
            * if x is not available (out of bounds): place 1.

4.  **Return:** Return the filled output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Bottom-Left Start
    output_grid[height - 1, 0] = 1

    # Iterative Pattern Filling
    for r in range(height - 1, -1, -1):
        for c in range(width):
            # Skip bottom-left
            if r == height - 1 and c == 0:
                continue

            if r == height - 1: #first row from bottom
              if c%2 == 0:
                output_grid[r,c] = 1
              else:
                output_grid[r,c] = 8
            else:
                y = output_grid[r+1,c]
                if y == 1:
                    output_grid[r,c] = 8
                elif y == 8:
                    if c > 0:
                        x = output_grid[r+1, c-1]
                        if x == 1:
                            output_grid[r,c] = 1
                        elif x == 8:
                            output_grid[r,c] = 8
                    else:
                        output_grid[r,c] = 1


    return output_grid
```