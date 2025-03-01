# 007bbfb7 • 011 • refine_coder

---
```python
"""
1. **Expansion:** Take the input grid and expand it by a factor of 3 in both dimensions. This creates a new, larger output grid.
2. **Yellow Block Creation:** For every yellow (4) pixel in the *input* grid, create a 3x3 block of yellow pixels in the *output* grid. The original yellow pixel's location in the input grid corresponds to the top-left corner of the 3x3 block in the output grid, after accounting for the 3x expansion. Specifically, if an input pixel is at `(r, c)`, the corresponding 3x3 block in the output grid starts at `(3r, 3c)`.
3. **Background Fill:** Fill any remaining cells in the output grid (those not part of a 3x3 yellow block) with black (0) pixels.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid: expand input by factor of 3
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 3, input_width * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Yellow Block Creation: iterate through input grid
    for r in range(input_height):
        for c in range(input_width):
            # check for yellow pixels
            if input_grid[r, c] == 4:
                # create 3x3 block in output grid, top-left at (3r, 3c)
                output_grid[r*3:r*3+3, c*3:c*3+3] = 4

    # Background Fill is handled by initialization of output_grid to all zeros

    return output_grid
```
