# 49d1d64f • 006 • refine_coder

---
```python
"""
Replicate each pixel from the input grid into a 2x2 block of the same color in an intermediate grid.
Add a one-pixel wide border of white (color 0) around the intermediate grid to create the final output grid.
"""

import numpy as np

def replicate_pixel(grid, row, col, output_grid):
    """Replicates a single pixel into a 2x2 block."""
    value = grid[row, col]
    output_grid[2*row:2*row+2, 2*col:2*col+2] = value
    return output_grid

def transform(input_grid):
    """Transforms the input grid according to the replication and bordering rule."""
    # Calculate intermediate grid dimensions (2x input).
    intermediate_height = 2 * input_grid.shape[0]
    intermediate_width = 2 * input_grid.shape[1]

    # Initialize intermediate_grid with the calculated dimensions.
    intermediate_grid = np.zeros((intermediate_height, intermediate_width), dtype=int)

    # Replicate each pixel of the input grid into the intermediate grid.
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            intermediate_grid = replicate_pixel(input_grid, row, col, intermediate_grid)

    # Calculate final output grid dimensions (intermediate + 2 for border).
    output_height = intermediate_height + 2
    output_width = intermediate_width + 2

    # Initialize output_grid with the calculated dimensions and fill with white (0).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the intermediate grid into the center of the output grid, leaving a 1-pixel border.
    output_grid[1:output_height-1, 1:output_width-1] = intermediate_grid

    return output_grid
```
