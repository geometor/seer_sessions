"""
The transformation rule identifies the first two distinct, horizontally adjacent colors in the input grid and uses them to form the 2x2 output grid. The first two distinct colors make the top row, and the next two make the second row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into a 2x2 output grid based on the first four
    distinct horizontally adjacent colors.
    """
    # Initialize an empty list to store the distinct color pairs.
    distinct_colors = []

    # Iterate through the input grid row by row.
    for row in input_grid:
        # Iterate through the cells of each row.
        previous_color = -1 # Initialize with a non-valid color
        for cell_color in row:
            if cell_color != previous_color:
                distinct_colors.append(cell_color)
                previous_color = cell_color
            if len(distinct_colors) == 4:
                break
        if len(distinct_colors) == 4:
            break

    # Create the 2x2 output grid.
    if len(distinct_colors) >= 4:
      output_grid = np.array(distinct_colors).reshape((2,2))

    elif len(distinct_colors) > 0 :
      output_grid = np.array(distinct_colors)
    else:
      output_grid = np.array([]) # empty grid
    

    return output_grid