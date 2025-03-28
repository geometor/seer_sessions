# 1b2d62fb • 020 • example_4 • investigate_coder

---
```python
"""
1.  **Identify the central blue column:** Find the vertical column of blue (1) pixels in the input grid.
2.  **Create an output grid:** Initialize a 5x3 output grid filled with white (0).
3. **Determine the adjacent pixels in input** Find the direct left and right neighbors of each pixel in the central column from the input grid.
4.  **Translate Neighbors to Output:**. In the *output grid*, change the color of the pixels corresponding to those positions in the input grid to azure (8), except for the first row where all is white.
5. **Other Input Pixels**: All other color pixels in input are transformed to white pixels in output at same position.
"""

import numpy as np

def find_blue_column(grid):
    # Find the column index where all elements are blue (1)
    rows, cols = grid.shape
    for j in range(cols):
        if all(grid[:, j] == 1):
            return j
    return -1  # Return -1 if no such column is found

def transform(input_grid):
    # initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, 3), dtype=int)

    # Find the central blue column
    blue_column_index = find_blue_column(input_grid)

    if blue_column_index != -1:
        # Iterate through each row
        for i in range(rows):
            # Set pixels adjacent to the blue column to azure (8), handling edge cases.
            if i > 0:
              if blue_column_index > 0 :
                  output_grid[i, 1 - (3- (blue_column_index-0)) ] = 8
              if blue_column_index < cols - 1:
                  output_grid[i, 1 + (blue_column_index + 1 - blue_column_index) ] = 8


    return output_grid
```
