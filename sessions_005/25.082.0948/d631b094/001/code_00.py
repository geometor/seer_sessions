"""
1.  **Identify the non-black color:** Examine the input grid and determine the single color value that is not 0.
2.  **Count the occurrences:** Count number of cells with the non-black color, save as N.
3.  **Create the output grid**: Create output of N of isolated color.
"""

import numpy as np

def get_non_black_color(grid):
    """Finds the non-black color in a grid."""
    for row in grid:
        for cell in row:
            if cell != 0:
                return cell
    return 0  # Should not reach here if there's always a non-black color

def transform(input_grid):
    # Find the non-black color
    non_black_color = get_non_black_color(input_grid)

    # Count the occurrences of the non-black color
    count = 0
    for row in input_grid:
        for cell in row:
            if cell == non_black_color:
                count += 1

    # Create the output grid
    output_grid = np.full((1, count), non_black_color)  #

    return output_grid