# 007bbfb7 • 016 • refine_coder

---
```python
"""
The transformation rule performs a pixel-by-pixel expansion of the input grid. Each pixel in the input grid is replaced by a 3x3 block of pixels of the *same* color in the output grid. The output grid's dimensions are three times the dimensions of the input grid. The color of each pixel in the input grid is preserved in the corresponding 3x3 block of the output grid.
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
            # Get the color of the current pixel.
            color = input_grid[i, j]
            # Replicate the pixel as a 3x3 block in the output grid.
            output_grid[i * 3:i * 3 + 3, j * 3:j * 3 + 3] = color

    return output_grid
```

