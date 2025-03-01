"""
The input grid is expanded to create an output grid. The expansion involves doubling the width of the input grid and adding two rows to the height. The colors on the border of the input grid are maintained and expanded outwards. The interior pixels of the input grid are replicated in the expanded area, effectively mirroring/copying the internal structure along the x-axis, and duplicating/smearing the top and bottom row into two rows each.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid dimensions.
    input_height, input_width = input_grid.shape
    output_height = input_height + 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy and expand the input grid along the x-axis (width).
    for i in range(input_height):
        for j in range(input_width):
            output_grid[i, j] = input_grid[i, j]
            output_grid[i, j + input_width] = input_grid[i, j]

    # Duplicate the top and bottom rows.
    output_grid[input_height, :] = output_grid[input_height-1, :]
    output_grid[input_height+1, :] = output_grid[0, :]
    
    return output_grid