# c59eb873 • 002 • example_3 • investigate_coder

---
```python
"""
The input grid is doubled in size, along both the horizontal and vertical axis, resulting in output that is increased on both dimensions x2.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating each pixel into a 2x2 block.
    """
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through input grid and replicate each pixel
    for row in range(input_height):
        for col in range(input_width):
            # Get the color of the current input pixel
            color = input_grid[row, col]

            # Calculate the top-left coordinates of the 2x2 block in the output grid
            output_row = row * 2
            output_col = col * 2

            # Fill the 2x2 block with the same color
            output_grid[output_row:output_row+2, output_col:output_col+2] = color

    return output_grid
```
