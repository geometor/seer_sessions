"""
Identify two colors that, when swapped, transform the input grid to the output grid. The transformation involves finding the cells with these two distinct colors and exchanging their positions in the grid. The colors to be swapped are determined by comparing the input and output grids and identifying the colors that have changed positions between the two.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the unique colors in the input grid.
    unique_colors = np.unique(input_grid)

    # Iterate through all possible pairs of distinct colors.
    for color1 in unique_colors:
        for color2 in unique_colors:
            if color1 != color2:
                # Create temporary grids for swapping.
                temp_grid = np.copy(input_grid)

                # Find positions of the two colors.
                pos1 = np.where(temp_grid == color1)
                pos2 = np.where(temp_grid == color2)

                # Swap the colors in the temporary grid.
                temp_grid[pos1] = color2
                temp_grid[pos2] = color1

                #Check to see if the temp grid matches the color2 position
                if np.array_equal(temp_grid[pos2], np.full_like(temp_grid[pos2], color1)):
                    # If a swap produces a valid intermediate, assign it and break.
                    output_grid = temp_grid
                    return output_grid

    return output_grid