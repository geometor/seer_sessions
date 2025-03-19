"""
The transformation rule is a color mapping applied to each pixel of a 2D grid.  The input grid's dimensions are preserved in the output grid. The following color substitutions are performed:

1. Red (2) is replaced with Magenta (6).
2. Green (3) is replaced with Yellow (4).
3. Azure (8) is replaced with Maroon (9).
Any other colors present in the input would remain unchanged. The size of the grid may vary.
"""

import numpy as np

def transform(input_grid):
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