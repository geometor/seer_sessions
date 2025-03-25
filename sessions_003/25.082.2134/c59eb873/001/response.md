```python
"""
The input grid is scaled up by a factor of 2. Each pixel in the input grid is
transformed into a 2x2 block of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through input grid and map each pixel to a 2x2 block in the output grid
    for i in range(input_height):
        for j in range(input_width):
            color = input_grid[i, j]
            # Set the 2x2 block in the output grid
            output_grid[2*i:2*i+2, 2*j:2*j+2] = color

    return output_grid
```