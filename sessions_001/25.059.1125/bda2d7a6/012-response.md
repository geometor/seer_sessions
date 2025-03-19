# bda2d7a6 • 012 • refine_coder

---
```python
"""
1.  **Identify the central 4x4 block:** Locate the contiguous 4x4 block within the input grid, defined by rows 2-5 (inclusive) and columns 2-5 (inclusive).
2.  **Color Inversion within Central Block:** Within this 4x4 central block:
    *   Change all orange (7) pixels to white (0).
    *   Change all magenta (6) pixels to orange (7).
3.  **Fill Surrounding Area:** Change all white (0) pixels in the region *outside* the 4x4 central block to magenta (6).
4. **Identify inner 2x2 block:** Locate the contiguous 2x2 block within the input grid, defined by rows 3-4 (inclusive) and columns 3-4 (inclusive). Note the colors are already correct in this area, so no operation is necessary.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Define the central block boundaries.
    central_block_start_row = 2
    central_block_end_row = 5
    central_block_start_col = 2
    central_block_end_col = 5

    # Iterate through the grid and apply transformations.
    for i in range(rows):
        for j in range(cols):
            # Fill surrounding area.
            if not (central_block_start_row <= i <= central_block_end_row and
                    central_block_start_col <= j <= central_block_end_col):
                if output_grid[i, j] == 0:
                    output_grid[i, j] = 6
            # Invert central block colors.
            else:
                if output_grid[i, j] == 7:
                    output_grid[i,j] = 0
                elif output_grid[i,j] == 6:
                    output_grid[i,j] = 7

    return output_grid
```

