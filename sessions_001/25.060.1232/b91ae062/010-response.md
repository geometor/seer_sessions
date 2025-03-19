# b91ae062 • 010 • example_2 • investigate_coder

---
```python
"""
Transforms a 3x3 input grid into a 6x6 output grid by expanding each pixel in the input to a 2x2 block of the same color in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Expands each pixel of the input grid into a 2x2 block in the output grid.
    """
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel in the input grid
    for row in range(input_height):
        for col in range(input_width):
            # Get the color of the current input pixel
            color = input_grid[row, col]

            # Create a 2x2 block in the output grid with the same color
            output_grid[2*row:2*row+2, 2*col:2*col+2] = color

    return output_grid
```
