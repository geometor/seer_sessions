# cce03e0d • 016 • refine_coder

---
```python
"""
The input grid is expanded into a larger output grid. The dimensions of the output grid are determined by multiplying both the height and width of the input grid by a factor of 3. The input grid is replicated within the output grid, both horizontally and vertically, according to this same factor (3). The remaining cells of the output grid, which are not part of the replicated input pattern, are filled with the background color, 0 (white).
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid.
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize the output grid with zeros.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate the input grid within the output grid.
    for row_mult in range(3):
        for col_mult in range(3):
            for i in range(input_height):
                for j in range(input_width):
                    output_grid[i + row_mult * input_height, j + col_mult * input_width] = input_grid[i, j]

    return output_grid
```

