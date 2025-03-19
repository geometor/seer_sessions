"""
The transformation rule is a color substitution applied to each pixel of the input grid. The following mapping is consistently used:

1.  Green (3) pixels are replaced with Yellow (4) pixels.
2.  Blue (1) pixels are replaced with Gray (5) pixels.
3.  Red (2) pixels are replaced with Magenta (6) pixels.

The dimensions and structure of the grid remain unchanged. The transformation is a direct, one-to-one substitution of color values, independent of pixel position.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Define the color mapping.
    color_map = {
        3: 4,  # Green to Yellow
        1: 5,  # Blue to Gray
        2: 6   # Red to Magenta
    }

    # Iterate through the grid and apply the mapping.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] in color_map:
                output_grid[i, j] = color_map[output_grid[i, j]]

    return output_grid