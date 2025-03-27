"""
The transformation rule identifies the first four distinct colors in the input grid, considering the order in which they first appear due to color transitions, and uses them to form the 2x2 output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into a 2x2 output grid based on the first four
    distinct colors, considering color transitions.
    """
    distinct_colors = []
    previous_color = -1  # Initialize with a non-valid color

    # Iterate through the input grid row by row.
    for row in input_grid:
        # Iterate through the cells of each row.
        for cell_color in row:
            # Check for color transition (distinct from the previous *distinct* color).
            if cell_color != previous_color:
                distinct_colors.append(cell_color)
                previous_color = cell_color  # Update the previous color
            # Stop if four distinct colors have been found
            if len(distinct_colors) == 4:
                break
        if len(distinct_colors) == 4:
            break

    # Create the 2x2 output grid.
    if len(distinct_colors) == 4:
        output_grid = np.array(distinct_colors).reshape((2, 2))
    elif len(distinct_colors) > 0:
        output_grid = np.array(distinct_colors) # return what colors exist
    else:
        output_grid = np.array([]) # return empty array

    return output_grid