# 007bbfb7 • 014 • example_3 • investigate_coder

---
```python
"""
The input grid is expanded by a factor of 3 in both dimensions. The positions of red(2) values in the input 3 x 3 are scaled up. For example, the pixel at (2,2) maps to (3*2, 3*2) which is (6,6).  All other remaining cells in the output are filled the with color white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with zeros, expanded by a factor of 3.
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 3, input_cols * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through the input grid.
    for i in range(input_rows):
        for j in range(input_cols):
            # If the current pixel is red (2), replicate it in the output grid.
            if input_grid[i, j] == 2:
                output_grid[i * 3, j * 3] = 2
                output_grid[i*3+2,j*3]=2
                output_grid[i*3,j*3+2]=2
                output_grid[i*3+2,j*3+2] =2


    return output_grid
```
