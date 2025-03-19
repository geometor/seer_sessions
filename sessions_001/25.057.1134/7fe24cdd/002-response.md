# 7fe24cdd • 002 • example_1 • investigate_coder

---
```python
"""
The input 3x3 grid is expanded into a 6x6 output grid. The original 3x3 grid becomes the top-left quadrant of the output grid. The output grid is then completed by reflecting the top-left quadrant horizontally, vertically, and diagonally.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 6x6 array filled with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Copy the input grid to the top-left quadrant of the output grid.
    output_grid[:rows, :cols] = input_grid

    # Horizontal reflection: Copy the top-left quadrant to the top-right quadrant.
    output_grid[:rows, cols:] = np.fliplr(input_grid)

    # Vertical reflection: Copy the top-left quadrant to the bottom-left quadrant.
    output_grid[rows:, :cols] = np.flipud(input_grid)

    # Diagonal reflection (Top-Left to Bottom-Right):
    output_grid[rows:, cols:] = np.fliplr(np.flipud(input_grid))

    return output_grid
```
