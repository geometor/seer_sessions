"""
The transformation rule involves a direct color substitution applied to each pixel independently. The spatial arrangement of the pixels remains unchanged (all grids are 3x3). Specifically:

1.  Any pixel that is red (color value 2) in the input grid becomes gray (color value 5) in the output grid.
2.  Any pixel that is green (color value 3) in the input grid becomes white (color value 0) in the output grid.
3. All other pixels retain their color.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid to maintain the same dimensions.
    output_grid = np.copy(input_grid)

    # Apply the color substitution rules:
    # Red (2) becomes gray (5).
    output_grid[input_grid == 2] = 5
    # Green (3) becomes white (0).
    output_grid[input_grid == 3] = 0

    return output_grid