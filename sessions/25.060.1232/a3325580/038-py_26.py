"""
1. Identify Objects: Examine the input grid and identify all contiguous regions of non-white (non-zero) pixels. Each of these regions constitutes an "object."
2. Extract Colors: For each identified object, record its color (pixel value). The relative position of the color to each other in the grid does not appear to matter.
3. Create Output Grid: Create a new output grid. Iterate through the input grid, if the pixel is one of the colors, then keep it, otherwise discard the value (which removes all 0's)
4. Determine new output dimensions. Create a new grid of those dimensions.
5. Fill the output grid: Place the color values from left-to-right, top-to-bottom
6. The output grid only contains the unique non-zero color values from input.
"""

import numpy as np

def get_unique_colors(grid):
    # get the unique colors in the input grid
    return np.unique(grid[grid != 0])

def transform(input_grid):
    # get unique colors, excluding white (0)
    unique_colors = get_unique_colors(input_grid)

    # create output grid based on the number of unique colors.
    num_colors = len(unique_colors)
    output_grid = np.zeros((num_colors, num_colors), dtype=int)

    #sort the colors
    sorted_colors = np.sort(unique_colors)

    #fill in the output grid in row major order
    output_grid = output_grid.reshape(-1)
    for index, val in enumerate(sorted_colors):
        output_grid[index%len(output_grid)] = val

    output_grid = output_grid.reshape(3, -1) #the result will always be a row vector

    return output_grid