# 46f33fce • 008 • refine_coder

---
```python
"""
Expands each non-white pixel in the input grid into a 2x2 square region of the same color in the output grid, effectively upscaling the input grid by a factor of 2 in both dimensions.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding each non-white pixel into a 2x2 square of the same color.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2, input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through the input grid to find non-white pixels
    for r in range(input_rows):
        for c in range(input_cols):
            pixel_color = input_grid[r, c]
            if pixel_color != 0:  # If not white
                # Expand the pixel into a 2x2 square in the output grid
                output_grid[2*r, 2*c] = pixel_color
                output_grid[2*r + 1, 2*c] = pixel_color
                output_grid[2*r, 2*c + 1] = pixel_color
                output_grid[2*r + 1, 2*c + 1] = pixel_color

    return output_grid
```

