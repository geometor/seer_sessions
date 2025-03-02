# 007bbfb7 • 032 • refine_coder

---
```python
"""
Expands each cell in the input grid into a 3x3 block of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with dimensions 3 times the input_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input_grid
    for i in range(input_height):
        for j in range(input_width):
            # Get the color of the current cell
            color = input_grid[i, j]

            # Fill the corresponding 3x3 block in output_grid with the same color
            for x in range(3):
                for y in range(3):
                    output_grid[i*3 + x, j*3 + y] = color

    return output_grid
```

