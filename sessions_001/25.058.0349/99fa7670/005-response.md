# 99fa7670 • 005 • refine_coder

---
```python
"""
The transformation rule involves taking the input grid, which consists of a single-color object, and stretching it horizontally. The output grid's width is double the input grid's width, while the height remains the same. The color of the object remains constant during the transformation. The operation can be described as horizontal stretching by a factor of 2.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by stretching it horizontally by a factor of 2.
    """
    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid.
    output_height = input_height
    output_width = input_width * 2

    # Create an output grid filled with zeros (white).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the input grid's contents to the output grid, stretching it horizontally.
    for row in range(input_height):
        for col in range(input_width):
            output_grid[row, col * 2] = input_grid[row, col]
            output_grid[row, col * 2 + 1] = input_grid[row, col]

    return output_grid
```

