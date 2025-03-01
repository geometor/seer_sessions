"""
Examine each training example's input and output grids.
If the output grid is identical to the input grid, no transformation is needed. Return the input grid.
If all pixels of a certain color in the input grid change to another single color in the output grid, then the transformation rule is to replace all instances of the first color with the second color.
If the position of pixels of a certain color change location from input to output, then that is a valid rule to try.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)

    # check if no transformation needed
    if np.array_equal(input_grid, output_grid):
        return output_grid

    # find unique colors in input and output
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    
    # check for color replacement
    for color1 in input_colors:
        if color1 not in output_colors: # Check if color1 is missing in output
           potential_replacement = None # Find color in output to replace
           for color2 in output_colors:
                if color2 not in input_colors: # Check if color 2 only in output
                    temp_grid = np.copy(input_grid)
                    temp_grid[temp_grid == color1] = color2
                    # check if the temp grid == output grid
                    if np.array_equal(temp_grid, output_grid):
                         return temp_grid


    # check simple swaps of 2 colors (from original code, kept as fallback)
    for color1 in input_colors:
        for color2 in input_colors:
            if color1 != color2:
                temp_grid = np.copy(input_grid)
                pos1 = np.where(temp_grid == color1)
                pos2 = np.where(temp_grid == color2)
                temp_grid[pos1] = color2
                temp_grid[pos2] = color1
                if np.array_equal(temp_grid, output_grid):
                    return temp_grid
    
    return output_grid