# 10fcaaa3 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Double Dimensions:** Double the height and width of the input grid.
2.  **Replicate Gray:** For every gray (5) pixel in the input, replicate its placement in the output, repeating the input grid a total of height times and length time.
3.  **Checkerboard Overlay**: Every other row alternate filling the first cell with an azure pixel, and blank.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # replicate gray pixels
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i, j] == 5:
                output_grid[i * 2, j * 2] = 5
                output_grid[i * 2 + 1, j * 2] = 5
                output_grid[i * 2, j * 2 + 1] = 5
                output_grid[i * 2 + 1, j * 2 + 1] = 5
    
    # checkerboard overlay
    for i in range(output_height):
        for j in range(output_width):
            if (i % 2 == 0) and (j % 2 == 0):
                output_grid[i,j] = 8

    return output_grid
```
