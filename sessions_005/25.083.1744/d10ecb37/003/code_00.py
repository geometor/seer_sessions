"""
The transformation rule identifies the first four distinct, horizontally adjacent colors in the input grid and uses them to form the 2x2 output grid. The first two distinct colors make the top row, and the next two make the second row, tracking transitions between colors.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into a 2x2 output grid based on the first four
    distinct horizontally adjacent colors, considering color transitions.
    """
    distinct_colors = []

    # Iterate through the input grid row by row.
    for row in input_grid:
        previous_color = -1  # Initialize with a non-valid color
        # Iterate through the cells of each row.
        for cell_color in row:
            # Check for color transition (distinct from the previous color).
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
        output_grid = np.array(distinct_colors)  # Handle cases with fewer than 4 colors
    else:
        output_grid = np.array([]) # Empty grid

    return output_grid