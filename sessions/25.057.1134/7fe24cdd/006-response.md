# 7fe24cdd • 006 • refine_coder

---
```python
"""
The transformation rule involves creating an output grid whose dimensions are derived from the input grid. The width of the output grid is always double the width of the input. The height of the output is double the input height for square grids, and remains the same for rectangular grids. The input grid's content is then copied and potentially reflected to fill the output grid. If the original grid is rectangular, the input is copied to fill the doubled width. If the input grid is square, the input is copied and reflected both horizontally and vertically, creating a symmetrical pattern.
"""

import numpy as np

def transform(input_grid):
    # Get input dimensions
    input_rows, input_cols = input_grid.shape

    # Determine output dimensions
    output_rows = input_rows * 2 if input_rows == input_cols else input_rows
    output_cols = input_cols * 2

    # Initialize output grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Handle square grids (reflection)
    if input_rows == input_cols:
        # Copy the input grid to the top-left quadrant of the output grid.
        output_grid[:input_rows, :input_cols] = input_grid

        # Horizontal reflection: Copy the top-left quadrant to the top-right quadrant.
        output_grid[:input_rows, input_cols:] = np.fliplr(input_grid)

        # Vertical reflection: Copy the top-left quadrant to the bottom-left quadrant.
        output_grid[input_rows:, :input_cols] = np.flipud(input_grid)

        # Diagonal reflection (Top-Left to Bottom-Right):
        output_grid[input_rows:, input_cols:] = np.fliplr(np.flipud(input_grid))
    # Handle rectangular grids (horizontal duplication)
    else:
        output_grid[:, :input_cols] = input_grid
        output_grid[:, input_cols:] = input_grid

    return output_grid
```
