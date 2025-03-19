# 10fcaaa3 • 004 • refine_coder

---
```python
"""
1.  **Double Dimensions:** Double the height and width of the input grid.
2.  **Replicate Gray:** For every gray (5) pixel in the input, create a 2x2 block of gray pixels in the output at the corresponding doubled coordinates.
3.  **Place Azure:** For every 2x2 block of grey pixels, place an azure (8) pixel directly above and directly to the left of it, if those positions are not occupied by grey.
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

    # place azure pixels
    for i in range(output_height):
        for j in range(output_width):
            if output_grid[i, j] == 5:
                # Check for top-left position relative to each gray pixel
                if i > 0 and j > 0 and output_grid[i - 1, j - 1] != 5:
                    output_grid[i - 1, j - 1] = 8
                # checking above
                elif i > 0 and output_grid[i-1,j] != 5:
                     if (i-1)%2 == 0 and j%2 == 0:
                        output_grid[i - 1, j ] = 8
                # checking left
                elif j > 0 and output_grid[i, j - 1] != 5:
                    if i%2 == 0 and (j - 1)%2 == 0:
                      output_grid[i, j - 1] = 8

    return output_grid
```
