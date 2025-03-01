# 0a938d79 • 006 • refine_coder

---
```python
"""
The transformation rule creates a 2x2 checkerboard pattern using red (2) and azure (8) in the output grid. The output grid has the same dimensions as the input grid. The checkerboard pattern consists of repeating blocks of:

2 8
8 2

The position of the non-zero pixels in the input grid is irrelevant to the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                output_grid[r, c] = 2  # Red
            else:
                output_grid[r, c] = 8  # Azure

    return output_grid
```
