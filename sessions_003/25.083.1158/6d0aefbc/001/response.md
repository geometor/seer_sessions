```python
"""
The input grid is expanded by a factor of 2 in both dimensions. Each pixel in the input is replicated to form a 2x2 square of the same color in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding it by a factor of 2 in both dimensions.  Each
    pixel in the input grid is replicated to form a 2x2 block in the output grid.
    """
    # Get dimensions of the input grid.
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Calculate dimensions of the output grid (double the input dimensions).
    output_height = 2 * input_height
    output_width = 2 * input_width

    # Initialize the output grid with zeros, using the calculated dimensions.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid.
    for y in range(input_height):
        for x in range(input_width):
            # Get the pixel value from the input grid.
            pixel_value = input_grid[y][x]

            # Map the input pixel to a 2x2 block in the output grid.
            output_grid[2 * y][2 * x] = pixel_value
            output_grid[2 * y + 1][2 * x] = pixel_value
            output_grid[2 * y][2 * x + 1] = pixel_value
            output_grid[2 * y + 1][2 * x + 1] = pixel_value

    return output_grid
```
