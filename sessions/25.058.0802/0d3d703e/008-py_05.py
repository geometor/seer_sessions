"""
Transforms a 3x3 input grid by mapping specific colors to new colors.

Input: A 3x3 grid with pixels of color red (2), green (3), or azure (8).
Transformation:
    - Red (2) becomes Magenta (6)
    - Green (3) becomes Yellow (4)
    - Azure (8) becomes Maroon (9)
Output: A 3x3 grid with the new colors.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a color mapping transformation to the input grid.
    """
    # Initialize the output grid with the same dimensions as the input.
    output_grid = np.copy(input_grid)

    # Define the color mapping.
    color_map = {
        2: 6,  # Red to Magenta
        3: 4,  # Green to Yellow
        8: 9   # Azure to Maroon
    }

    # Iterate through each pixel in the grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Get the color of the current pixel.
            current_color = input_grid[i, j]

            # Apply color mapping if the current color is in the map.
            if current_color in color_map:
                output_grid[i, j] = color_map[current_color]

    return output_grid