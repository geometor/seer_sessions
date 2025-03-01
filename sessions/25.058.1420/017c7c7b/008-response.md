# 017c7c7b • 008 • example_1 • investigate_coder

---
```python
"""
Expands the input grid vertically by a factor of 1.5 and substitutes blue (1) pixels with red (2) pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid. The output grid width is the same as the input,
    # and height is 1.5 times the input height.
    input_height, input_width = input_grid.shape
    output_height = int(input_height * 1.5)
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid and map values to the output.
    for r in range(input_height):
        for c in range(input_width):
            output_row = int(r * 1.5)
            if input_grid[r, c] == 1:  # If blue
                output_grid[output_row, c] = 2  # Change to red
            else:  # if white
                output_grid[output_row,c] = input_grid[r,c] # copy the value (which is 0)
                
    return output_grid
```
