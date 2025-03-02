# 794b24be • 040 • refine_coder

---
```python
"""
Iterate through every pixel in the input grid. If a pixel is blue, change it to red in the output grid. All other pixels in the input grid remain the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions and data type as the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through all rows and columns of the input grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Check if the current pixel is blue (1).
            if input_grid[i, j] == 1:
                # Change the corresponding pixel in the output grid to red (2).
                output_grid[i, j] = 2

    return output_grid
```

