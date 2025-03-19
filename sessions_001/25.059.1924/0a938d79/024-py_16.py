"""
1.  **Identify Non-Zero Pixels:** Locate all pixels in the input grid that have a non-zero color value.
2.  **Propagate Color:** For each non-zero pixel (or group of adjacent non-zero pixels of the same color), take the color value.
3. **Fill Output:** Create an output grid of the same size as the input grid and fill every cell of the output grid with the color from step 2. If there are multiple non-zero colors, they do not interact/mix - the last processed non-zero group determines the grid color.
"""

import numpy as np

def get_last_non_zero_color(grid):
    # Iterate in reverse to find the last non-zero color
    grid = np.array(grid)
    for row in reversed(grid):
        for pixel in reversed(row):
            if pixel != 0:
                return pixel
    return 0  # Return 0 if no non-zero color is found

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Get the last non-zero color in the input grid
    last_color = get_last_non_zero_color(input_grid)

    # Fill the output grid with the last non-zero color
    output_grid[:] = last_color

    return output_grid.tolist()