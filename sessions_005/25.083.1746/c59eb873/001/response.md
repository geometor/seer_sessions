```python
"""
Each pixel in the input grid is expanded into a 2x2 block of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = 2 * input_height
    output_width = 2 * input_width

    # Initialize output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel in the input grid
    for row in range(input_height):
        for col in range(input_width):
            # Get the color of the current input pixel
            color = input_grid[row, col]

            # Calculate the top-left corner coordinates of the 2x2 block in the output grid
            output_row = 2 * row
            output_col = 2 * col

            # Fill the 2x2 block in the output grid with the same color
            output_grid[output_row:output_row+2, output_col:output_col+2] = color

    return output_grid
```