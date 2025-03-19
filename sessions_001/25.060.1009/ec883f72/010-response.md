# ec883f72 • 010 • refine_coder

---
```python
"""
The transformation rule adds a two-pixel green "L" shape to the input grid. The output grid is created by adding a column to the input grid. The "L" shape is placed in the top right corner of the output grid, with one pixel in the first row and last column, and the other pixel directly below it.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input grid.
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Create an output grid that's one column wider than the input.
    output_width = input_width + 1
    output_height = input_height
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the input grid to the output grid.
    output_grid[:, :input_width] = input_grid
    
    # Add the green "L" shape in the top right corner.
    output_grid[0, output_width - 1] = 3
    output_grid[1, output_width - 1] = 3

    return output_grid
```
