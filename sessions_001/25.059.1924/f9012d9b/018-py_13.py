"""
1. Identify Unique Colors: Examine the input grid and determine the unique colors present, excluding white (0).
2. Create Output Grid: Create a 2x2 output grid.
3. Populate Grid:
    *   If only one unique color (excluding white) exists, fill the entire 2x2 grid with that color.
    *   If two or more unique colors (excluding white) exist:
        *   Fill the top-left, top-right and bottom-left cells with the first unique color.
        *    Fill the bottom-right cell with the second unique color.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_array = np.array(input_grid)

    # 1. Identify Unique Colors (excluding white/0).
    unique_colors = np.unique(input_array)
    filtered_colors = [color for color in unique_colors if color != 0]

    # 2. Create Output Grid (2x2).
    output_grid = np.zeros((2, 2), dtype=int)

    # 3. Populate Grid.
    if len(filtered_colors) > 0:
        first_color = filtered_colors[0]
        output_grid[:, :] = first_color  # Fill the entire grid initially

        if len(filtered_colors) > 1:
            second_color = filtered_colors[1]
            output_grid[1, 1] = second_color  # Overwrite bottom-right if a second color exists

    return output_grid.tolist()