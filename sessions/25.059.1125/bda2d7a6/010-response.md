# bda2d7a6 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify the central block:**  Locate the contiguous 4x4 block within the input grid, rows 2-5 and cols 2-5.
2. **Identify the inner block:** Locate the contiguous 2x2 block within the input grid, rows 3-4 and cols 3-4.
3.  **Invert Central Block Colors:** Within the 4x4 central block identified in step 1:
    *   Change all orange (7) pixels to white (0).
    *   Change all magenta (6) pixels to orange (7).
4.  **Fill Surrounding Area:** Change all white (0) pixels in the *rest* of the grid (the area *outside* of the 4x4 central block) to magenta (6).
5. The output should be a grid with an outer area of magenta, a 2x2 square of orange, and the balance of the central 4x4 block white.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Define the central block boundaries.
    central_block_start_row = 1
    central_block_end_row = 4
    central_block_start_col = 1
    central_block_end_col = 4

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
