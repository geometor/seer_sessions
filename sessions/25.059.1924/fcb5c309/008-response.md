# fcb5c309 • 008 • refine_coder

---
```python
"""
1.  **Initialization:** Create an output grid with the same dimensions as the input grid, initially filled with zeros.
2.  **Border Creation:** Fill the outermost border of the output grid with yellow (4) pixels. This means all pixels in the first and last rows, and the first and last columns, are set to 4.
3.  **Inner Pixel Transformation:** Iterate through each pixel of the *input* grid that is *not* on the border.
    *   If the pixel's value in the input grid is 0 (white), set the corresponding pixel in the output grid to 0 (white).
    *   If the pixel's value in the input grid is not 0 (not white), copy the value *unchanged* to the corresponding pixel in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # change output pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            # Fill border with yellow
            if (r == 0 or r == input_grid.shape[0] - 1 or
                c == 0 or c == input_grid.shape[1] - 1):
                output_grid[r, c] = 4
            # Inner pixel transformation
            elif input_grid[r,c] == 0:
                output_grid[r,c] = 0
            else:
                output_grid[r, c] = input_grid[r,c]

    return output_grid.tolist()
```
