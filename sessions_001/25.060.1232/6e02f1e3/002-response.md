# 6e02f1e3 • 002 • example_5 • investigate_coder

---
```python
"""
1.  **Initialization:** Create an output grid of the same dimensions as the input grid (3x3), initially filled with 0s.

2.  **Check input grid color pattern:**.
    *   If all pixels of input have the same color, the output is a horizontal line of grey (5) in the first row.
    *   Otherwise, put grey color (5) in the output according these rules:
        *   If the top-left pixel is different in color to both the top-center and left-center pixels, construct a diagonal from the top-left to the bottom-right of grey (5) pixels.
        *    If the top-right pixel is different in color to both the top-center and right-center pixels, construct a diagonal from the top-right to bottom-left of grey (5) pixels.
        *   Otherwise, if only the colors in the first row are different, construct a diagonal from the top-left to the bottom-right of grey (5) pixels.

3.  **Color Transformation:**
    *   Replace the pixels in the output grid with the gray color (5)

"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    output_grid = np.zeros_like(input_grid)
    input_arr = np.array(input_grid)

    # Check if all pixels have the same color
    if np.all(input_arr == input_arr[0, 0]):
        output_grid[0, :] = 5  # Fill the first row with grey
        return output_grid

    # Check for diagonal conditions
    if (input_arr[0, 0] != input_arr[0, 1]) and (input_arr[0, 0] != input_arr[1, 0]):
       output_grid[0, 0] = 5
       output_grid[1, 1] = 5
       output_grid[2, 2] = 5
    elif (input_arr[0, 2] != input_arr[0, 1]) and (input_arr[0, 2] != input_arr[1, 2]):
        output_grid[0, 2] = 5
        output_grid[1, 1] = 5
        output_grid[2, 0] = 5
    elif not np.array_equal(input_arr[0,:], [input_arr[0,0]] * 3):
       output_grid[0, 0] = 5
       output_grid[1, 1] = 5
       output_grid[2, 2] = 5
    else:
        output_grid[0, 0] = 5
        output_grid[1, 1] = 5
        output_grid[2, 2] = 5

    return output_grid
```
