# cce03e0d • 006 • refine_coder

---
```python
"""
The output grid's height is three times the input grid's height. The output grid's width is equal to the input grid's width, plus the number of example pairs. The input grid is embedded into the output grid starting at a row index equal to the input grid's height and a column index of 0. The rest of the output grid is filled with white (color 0).
"""

import numpy as np

def transform(input_grid):
    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Calculate output dimensions
    output_height = input_height * 3
    output_width = input_width + 4  # add number of additional examples (5-1=4)

    # Create an output grid filled with white (0).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Calculate the starting row index for embedding.
    start_row = input_height
    start_col = 0

    # Embed the input grid into the output grid.
    output_grid[start_row:start_row + input_height, start_col:start_col + input_width] = input_grid

    return output_grid
```

