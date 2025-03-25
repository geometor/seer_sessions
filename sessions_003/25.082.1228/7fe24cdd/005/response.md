```python
"""
1.  **Expand Grid:** Create an output grid with dimensions twice the height and twice the width of the input grid.
2.  **Copy Top-Left:** Copy the input grid directly to the top-left quadrant of the output grid.
3.  **Mirror Top-Right:** Flip the input grid along the bottom-left to top-right diagonal (swap rows and columns and mirror), and copy the result to the top-right quadrant.
4.  **Mirror Bottom-Left:** Flip the input grid along the top-left to bottom-right diagonal (swap rows and columns), and copy the result to the bottom-left quadrant.
5.  **Mirror Bottom-Right:** Rotate the input grid 180 degrees and copy it to the bottom-right quadrant.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy Top-Left
    output_grid[:input_height, :input_width] = input_grid

    # Mirror Top-Right: Diagonal flip (bottom-left to top-right)
    output_grid[:input_height, input_width:] = np.fliplr(input_grid).T

    # Mirror Bottom-Left: Diagonal flip (top-left to bottom-right)
    output_grid[input_height:, :input_width] = np.flipud(input_grid).T

    # Mirror Bottom-Right: 180-degree rotation
    output_grid[input_height:, input_width:] = np.rot90(input_grid, 2)

    return output_grid.tolist()
```