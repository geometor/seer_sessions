```python
"""
1.  **Expand Grid:** The input grid is expanded to an output grid with twice the height and twice the width.
2.  **Copy Top-Left:** The input grid is copied directly into the top-left quadrant of the output grid.
3.  **Mirror Top-Right:** The input grid is horizontally flipped (columns are reversed) and copied to the top-right quadrant of the output grid.
4.  **Mirror Bottom-Left:** The input grid is vertically flipped (rows are reversed) and copied to the bottom-left quadrant of the output grid.
5.  **Mirror Bottom-Right:** The input grid is both horizontally and vertically flipped (rows and columns are reversed, equivalent to a 180-degree rotation) and copied to the bottom-right quadrant of the output grid.
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

    # Mirror Top-Right
    output_grid[:input_height, input_width:] = np.fliplr(input_grid)

    # Mirror Bottom-Left
    output_grid[input_height:, :input_width] = np.flipud(input_grid)

    # Mirror Bottom-Right
    output_grid[input_height:, input_width:] = np.flipud(np.fliplr(input_grid))

    return output_grid.tolist()
```