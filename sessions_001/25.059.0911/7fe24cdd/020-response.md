# 7fe24cdd • 020 • example_3 • investigate_coder

---
```python
"""
Expands the input grid to double its size in both dimensions and fills the expanded grid by mirroring the original pixel values in both horizontal and vertical directions, creating a checkerboard pattern.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Calculate dimensions of the output grid
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with zeros
    output_grid = [[0] * output_width for _ in range(output_height)]

    # Iterate through the input grid and mirror the values to the output grid
    for row in range(input_height):
        for col in range(input_width):
            # Get the pixel value from the input grid
            pixel_value = input_grid[row][col]

            # Mirror the pixel value to the four corresponding positions in the output grid
            output_grid[row][col] = pixel_value
            output_grid[row][col + input_width] = pixel_value
            output_grid[row + input_height][col] = pixel_value
            output_grid[row + input_height][col + input_width] = pixel_value

    return output_grid
```
