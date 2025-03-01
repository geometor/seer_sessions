"""
The task involves transforming a grid of colored pixels. The primary colors
involved are red, white, azure, and blue. The transformation rule depends on
the spatial relationship between red pixels and white pixels. White pixels to
the right of any red pixel are changed to azure, and white pixels to the left
of any red pixel are changed to blue.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all red pixels
    red_pixels = np.argwhere(input_grid == 2)

    # Iterate through the grid and change colors based on the position relative to the red pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:  # If it's white
                is_right = False
                is_left = False
                for red_r, red_c in red_pixels:
                    if c > red_c:
                        is_right = True
                    if c < red_c:
                        is_left = True
                if is_right:
                    output_grid[r, c] = 8  # Change to azure
                elif is_left:
                    output_grid[r, c] = 1  # Change to blue

    return output_grid