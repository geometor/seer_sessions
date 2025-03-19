# 91413438 • 024 • refine_coder

---
```python
"""
The input grid is replicated exactly once horizontally, effectively doubling its width. If the input's width is greater than or equal to 9, the width is extended to 18 by adding white pixels.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Double the width by replicating the input grid horizontally.
    output_width = input_width * 2
    output_grid = np.tile(input_grid, (1, 2))
    
    # Handle edge case for input width >= 9.
    if input_width >= 9:
        output_width = 18
        output_grid = np.zeros((input_height, output_width), dtype=int)
        output_grid[:, :input_width] = input_grid
        # extend by repeating last column
        output_grid[:,input_width:] = np.tile(input_grid[:, -1:], (1,18-input_width))

    return output_grid
```
