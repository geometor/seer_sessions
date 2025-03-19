# ed36ccf7 • 004 • refine_coder

---
```tool_code
"""
The transformation takes a 3x3 input grid containing a 1x2 or 2x1 block of white pixels (0) and outputs a 3x3 grid where the white block is always positioned at the top-left corner, and the rest of the grid is filled with maroon pixels (9). The orientation of the white block does not affect the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with maroon pixels.
    output_grid = np.full((3, 3), 9)

    # Place the white pixels at the top-left.
    output_grid[0, 0] = 0
    output_grid[1, 0] = 0

    return output_grid
```
