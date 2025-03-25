"""
1. **Examine the input grid:** Consider all colors present within the input grid.
2. **Identify the target color:** Determine the color that appears exactly three times within the input grid.
3. **Create the output grid:** Create an output grid with the same dimensions as the input grid.
4. **Fill output grid:** Fill every cell of the output grid with the target color identified in step 2.
"""

import numpy as np

def transform(input_grid):
    # Create output grid of same dimensions.
    output_grid = np.zeros_like(input_grid)

    # Count the occurrences of each color in the input grid
    color_counts = {}
    for color in np.unique(input_grid):
        color_counts[color] = np.count_nonzero(input_grid == color)

    # Find the color that appears exactly three times
    target_color = None
    for color, count in color_counts.items():
        if count == 3:
            target_color = color
            break

    # Fill the output grid with the target color
    if target_color is not None:  # Added a check in case no color appears exactly 3 times
      output_grid[:] = target_color

    return output_grid