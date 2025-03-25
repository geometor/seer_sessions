```python
"""
The input grid's dimensions are doubled to create the output grid. Each pixel from the input grid at (i, j) is mapped to the output grid at (2i, 2j). Additionally, if a pixel's value isn't 0, it's also mapped to (2i + (j+1)%2, 2j + (i+1)%2). If it is zero, it is mapped to (2i + (j)%2, 2j + (i)%2)
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with zeros, double the size of input_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Iterate through each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            pixel_value = input_grid[i, j]

            # Map to the (2i, 2j) position
            output_grid[2 * i, 2 * j] = pixel_value

            # Additional mapping based on interleaving and 0 condition
            if pixel_value != 0:
                output_grid[2 * i + (j + 1) % 2, 2 * j + (i + 1) % 2] = pixel_value
            else:
                output_grid[2 * i + (j) % 2, 2 * j + (i) % 2] = pixel_value
    return output_grid
```