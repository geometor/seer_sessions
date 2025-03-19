# a85d4709 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Initialization:** Start with a 3x3 input grid. The output grid will also be 3x3.

2.  **Pixel-wise Transformation:** For each pixel in the input grid:

    *   If the pixel value is 0, change that pixel in the output grid to 3.
    *   If the pixel value is 5, and at the center position (row 1, column 1) then the corresponding output pixel is assigned the value 4.
    *   If the pixel value is 5, and at the corner positions (row 0 column 0, row 0 column 2, row 2, column 0, and row 2, column2), then the corresponding output pixel is assigned the value of 2.

3.  **Output:** The transformed 3x3 grid is the final output.
"""

import numpy as np

def transform(input_grid):
    """Transforms a 3x3 input grid to a 3x3 output grid based on specific rules.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:
                output_grid[i, j] = 3
            elif input_grid[i, j] == 5:
                if i == 1 and j == 1:  # Center position
                    output_grid[i, j] = 4
                elif (i == 0 and j == 0) or \
                     (i == 0 and j == 2) or \
                     (i == 2 and j == 0) or \
                     (i == 2 and j == 2):  # Corner positions
                    output_grid[i, j] = 2
    return output_grid
```
