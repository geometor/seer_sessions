# d10ecb37 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation extracts the top-left quadrant of the input grid to create the output grid. The output grid's dimensions are one-third the size of the input grid's dimensions.
"""

import numpy as np

def transform(input_grid):
    # Determine output dimensions.
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = input_height // 3
    output_width = input_width // 3

    # Initialize output_grid.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Extract subgrid.
    for row in range(output_height):
        for col in range(output_width):
            output_grid[row][col] = input_grid[row][col]

    return output_grid
```
