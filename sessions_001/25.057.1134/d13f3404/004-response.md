# d13f3404 • 004 • refine_coder

---
```python
"""
The input grid is transformed into an output grid with double the dimensions. Each non-white pixel in the input grid generates a single-pixel diagonal line of the same color in the output grid. The diagonal starts at the doubled coordinates of the input pixel. The direction of the diagonal varies depending on the example.
"""

import numpy as np

def determine_direction(example_index, input_row, input_col):
    """
    Determines the direction of the diagonal based on the example index and input coordinates.
    """
    if example_index == 0:  # Example 1: down-right
        return 1, 1
    elif example_index == 1:  # Example 2: down-right
        return 1, 1
    elif example_index == 2:  # Example 3: down-left
        return 1, -1
    elif example_index == 3: # Example 4: up-right
        return -1, 1
    else:
        return 1,1 # default to down, right

def transform(input_grid, example_index):
    # initialize output_grid with double the dimensions, filled with white (0)
    input_rows, input_cols = len(input_grid), len(input_grid[0])
    output_rows, output_cols = 2 * input_rows, 2 * input_cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # iterate through each pixel of the input grid
    for i in range(input_rows):
        for j in range(input_cols):
            pixel_color = input_grid[i][j]
            # if the pixel is not white
            if pixel_color != 0:
                # calculate the starting position in the output grid (doubled coordinates)
                start_row, start_col = 2 * i, 2 * j
                
                # determine direction
                d_row, d_col = determine_direction(example_index, i, j)

                # draw a single pixel diagonal line
                row, col = start_row, start_col
                
                if 0 <= row + d_row < output_rows and 0 <= col + d_col < output_cols:
                    output_grid[row + d_row][col + d_col] = pixel_color

    return output_grid
```
