# 6150a2bd • 014 • example_2 • investigate_coder

---
```python
"""
1. **Identify Non-Zero Pixels:** Locate all pixels in the input grid that have a value other than 0 (white).

2.  **Mirror, Top to Bottom:** The values in the top row of the input are mirrored to the bottom row of the output.

3. **Mirror, Left to Right:** The Values in the leftmost column of the input are mirrored to the rightmost column of the output.

4. **Preserve Zeroes:** Maintain the locations all of the zero (white) cells.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # get dimensions
    rows, cols = input_grid.shape

    # Preserve Zeroes:  Iterate through all cells
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:
                output_grid[i, j] = 0  # Keep 0s in place
            else:
                output_grid[i,j] = 0


    # Mirror, Top to Bottom
    for j in range(cols):
        output_grid[rows - 1, j] = input_grid[0, j]

    # Mirror, Left to Right
    for i in range(rows):
        output_grid[i, cols-1] = input_grid[i,0]

    return output_grid
```
