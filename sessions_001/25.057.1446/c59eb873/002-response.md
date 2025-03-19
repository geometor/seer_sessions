# c59eb873 • 002 • example_1 • investigate_coder

---
```python
"""
Scales up the input grid by a factor of 2. Each pixel in the input grid is 
represented as a 2x2 block of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels 
    for row in range(input_height):
        for col in range(input_width):
            # Get the color value of the current input cell.
            color = input_grid[row, col]
            
            # Fill a 2x2 block in the output grid with the color value.
            output_grid[2*row, 2*col] = color
            output_grid[2*row + 1, 2*col] = color
            output_grid[2*row, 2*col + 1] = color
            output_grid[2*row + 1, 2*col + 1] = color

    return output_grid
```
