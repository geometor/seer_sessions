# 3af2c5a8 • 006 • refine_coder

---
```python
"""
1. Expansion: The input grid is expanded to create an output grid that is double the height and double the width of the input grid.
2. Pixel Replication: Each individual pixel in the input grid is transformed into a 2x2 block of pixels of the same color in the output grid. For example, an azure pixel at position (0, 0) in the input becomes a 2x2 block of azure pixels at positions (0, 0), (0, 1), (1, 0), and (1, 1) in the output. This replication applies to all pixels, regardless of their color.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the 2x2 replication rule."""
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows * 2
    output_cols = input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through each pixel of the input grid
    for i in range(input_rows):
        for j in range(input_cols):
            # Get the color of the current pixel
            color = input_grid[i, j]
            # Replicate the pixel into a 2x2 block in the output grid
            output_grid[2*i:2*i+2, 2*j:2*j+2] = color

    return output_grid
```

