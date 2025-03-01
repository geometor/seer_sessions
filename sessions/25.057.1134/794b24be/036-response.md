# 794b24be • 036 • refine_coder

---
```python
"""
Iterate through every pixel of the input grid.
Check the color of the input pixel.
Apply the following color mapping rules:
    If the input pixel is blue (1), change it to red (2) in the output grid.
    If the input pixel is green (3), change it to yellow (4) in the output grid.
    If the input pixel is black(0), change it to black(0) in the output grid.
Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Iterate through each pixel in the grid
    for i in range(rows):
        for j in range(cols):
            # Check the color of the input pixel and apply color mapping
            if input_grid[i, j] == 1:
                output_grid[i, j] = 2
            elif input_grid[i, j] == 3:
                output_grid[i, j] = 4
            elif input_grid[i, j] == 0:
                output_grid[i,j] = 0

    return output_grid
```

