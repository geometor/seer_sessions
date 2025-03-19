"""
The transformation rule is a simple color substitution applied uniformly across the entire input grid.  The following color mappings are applied:

*   Maroon (9) is replaced with Azure (8).
*   Yellow (4) is replaced with Green (3).
*   Red (2) is replaced with Magenta (6).
*   All other colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Create a color mapping dictionary for the substitutions
    color_map = {
        9: 8,  # Maroon to Azure
        4: 3,  # Yellow to Green
        2: 6   # Red to Magenta
    }

    # Iterate through each cell in the grid
    for row_index, row in enumerate(output_grid):
        for col_index, pixel_value in enumerate(row):
            # Check if the pixel's color needs to be changed based on color_map
            if pixel_value in color_map:
                # Apply the color substitution
                output_grid[row_index, col_index] = color_map[pixel_value]

    return output_grid