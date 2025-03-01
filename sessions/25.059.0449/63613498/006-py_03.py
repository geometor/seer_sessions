"""
The transformation rule is a color substitution rule. Pixels that are magenta (6), maroon (9), or yellow (4) in the input grid are changed to gray (5) in the output grid. All other colors, including and specifically blue(1) remain unchanged. The spatial arrangement of pixels is preserved; only the color values are altered according to this rule.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the output grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Change pixel color based on the transformation rules
            if output_grid[i, j] == 6:  # Magenta
                output_grid[i, j] = 5  # Gray
            elif output_grid[i, j] == 9:  # Maroon
                output_grid[i, j] = 5  # Gray
            elif output_grid[i, j] == 4:  # Yellow
                output_grid[i, j] = 5  # Gray
            # All other colors remain unchanged

    return output_grid