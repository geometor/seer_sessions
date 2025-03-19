# 46442a0e • 012 • refine_coder

---
```python
"""
Scale up the input grid by a factor of 2 in both dimensions. Each pixel in the input grid corresponds to a 2x2 block of pixels of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Create a new grid with dimensions scaled up by a factor of 2.
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Iterate through each pixel of the input grid.
    for i in range(rows):
        for j in range(cols):
            # Get the color of the current pixel.
            color = input_grid[i, j]

            # Create a 2x2 block in the output grid with the same color.
            output_grid[i*2:i*2+2, j*2:j*2+2] = color

    return output_grid
```

