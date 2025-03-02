# b8cdaf2b • 004 • refine_coder

---
```python
"""
Copies the input grid to the output grid. 
Iterates through the grid starting from the third-to-last row, moving upwards.
If a pixel is white (0), it checks the pixel two rows below. 
If that pixel has color x, *and* the row two rows below is NOT the bottom row, the current pixel is replaced with x. 
If the row two rows below is the bottom row, then copy the bottom row to every row above.

"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check if the bottom row is different from the second-to-last row
    bottom_row_unique = not np.array_equal(input_grid[-1, :], input_grid[-2, :])

    # Iterate upwards from the third-to-last row
    for i in range(rows - 3, -1, -1):
        for j in range(cols):
            # Conditional Color Change
            if output_grid[i, j] == 0:  # If the current pixel is white
                if i + 2 == rows - 1: # two rows below is second to last
                    if bottom_row_unique: # and bottom row is unique
                        output_grid[:rows-1,:] = input_grid[-1,:] # populate with the bottom row values
                        return output_grid # return the populated grid (special case)
                elif i + 2 < rows:
                    output_grid[i,j] = input_grid[i+2,j]

    return output_grid
```
