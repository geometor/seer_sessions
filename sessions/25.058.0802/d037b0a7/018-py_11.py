"""
The output grid is a copy of the input grid. All non-white pixels in the input grid are replaced by a single color in the output grid. The replacement color is consistent within each output grid but varies between different examples. White pixels remain unchanged.
"""

import numpy as np

def get_replacement_color(input_grid, output_grid):
    # Find a non-white pixel in the output grid to determine the replacement color.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] != 0 and input_grid[i,j] != 0:
                return output_grid[i, j]
    return 0  # Default to white if no replacement color is found (shouldn't happen in valid cases)

def transform(input_grid, output_grid):
    # Create a copy of the input grid.
    output_grid_copy = np.copy(input_grid)

    # Determine the replacement color.
    replacement_color = get_replacement_color(input_grid, output_grid)


    # Iterate through the input grid and replace colors in the output grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != 0:  # If not white
                output_grid_copy[i, j] = replacement_color  # Replace with the replacement color

    return output_grid_copy