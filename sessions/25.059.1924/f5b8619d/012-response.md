# f5b8619d • 012 • refine_coder

---
```python
"""
The transformation expands the original image by surrounding each original pixel with light blue and preserving the position of the original gray.
Add an additional white border to the resulting image. The output grid's dimensions are calculated as follows: output_dimension = (2 * input_dimension) + 3.
Original pixel at [r, c] in the input goes to [2*r + 2, 2*c + 2] in the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = (2 * input_rows) + 3, (2 * input_cols) + 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)
    
    # Add white border
    output_grid[:] = 0

    # fill remaining cells with azure (8)
    output_grid[1:output_rows-1, 1:output_cols-1] = 8

    # replace the original colors in the expanded grid, keeping the relative position
    for r in range(input_rows):
        for c in range(input_cols):
            output_grid[2*r + 2, 2*c + 2] = input_grid[r,c]


    return output_grid
```

