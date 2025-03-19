"""
The transformation rule is a color mapping applied to each pixel of the input grid. The grid dimensions remain constant. The specific color mappings are:

1.  Red pixels are changed to White.
2.  Yellow pixels are changed to Gray.
3.  Maroon pixels are changed to Gray.
4.  All other colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy to modify
    output_grid = input_grid.copy()

    # change output pixels based on color mapping
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 2:  # Red
                output_grid[i, j] = 0  # White
            elif output_grid[i, j] == 4:  # Yellow
                output_grid[i, j] = 5  # Gray
            elif output_grid[i, j] == 9:  # Maroon
                output_grid[i, j] = 5  # Gray
    return output_grid