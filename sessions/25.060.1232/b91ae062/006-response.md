# b91ae062 • 006 • refine_coder

---
```python
"""
The input grid is scaled up by a factor of 2 in both dimensions. Each pixel in the input grid is replaced by a 2x2 block of pixels of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with doubled dimensions
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel in the input grid
    for row in range(input_height):
        for col in range(input_width):
            # Replicate the pixel's color to form a 2x2 block
            output_grid[row*2:row*2+2, col*2:col*2+2] = input_grid[row, col]

    return output_grid
```

