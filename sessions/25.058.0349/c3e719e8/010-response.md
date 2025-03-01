# c3e719e8 • 010 • refine_coder

---
```python
"""
The input grid is quadrupled by mirroring it both horizontally and vertically.  A single row of zeros is inserted between the top and bottom copies, and a single column of zeros is inserted between the left and right copies.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions: twice the input plus one for the separator row/column.
    output_height = 2 * input_height + 1
    output_width = 2 * input_width + 1

    # Initialize output_grid as calculated dimensions filled with 0s
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place the input grid in the top-left corner
    output_grid[:input_height, :input_width] = input_grid

    # Place the mirrored input grid in the top-right corner
    output_grid[:input_height, input_width + 1:] = input_grid

    # Place the mirrored input grid in the bottom-left corner
    output_grid[input_height + 1:, :input_width] = input_grid

    # Place the mirrored input grid in the bottom-right corner
    output_grid[input_height + 1:, input_width + 1:] = input_grid

    return output_grid
```

