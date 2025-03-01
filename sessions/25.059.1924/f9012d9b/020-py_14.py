"""
1. Identify Unique Colors: Examine the input grid and determine the unique colors present, excluding white (0).
2. Create Output Grid: Create a 2x2 output grid.
3. Populate Grid:
    *   If only one unique color (excluding white) exists, fill the entire 2x2 grid with that color.
    *   If two unique colors (excluding white) exist:
        *   Examine the relative positions of colored areas in the input.
        *   Fill the top-left, top-right and bottom-left cells with the color that appears first in a raster scan (left-to-right, top-to-bottom) of the input grid.
        *    Fill the bottom-right cell with the color that appears second in the raster scan.

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
            second_color = None
            # Find the first occurrence of each color
            first_color_pos = np.where(input_array == first_color)
            first_color_idx = (first_color_pos[0][0], first_color_pos[1][0])
            
            for color in filtered_colors[1:]:
              color_pos = np.where(input_array == color)
              color_idx = (color_pos[0][0], color_pos[1][0])
              if color_idx < first_color_idx:
                second_color = first_color
                first_color = color
                first_color_idx = color_idx
              elif second_color is None:
                second_color = color
              else:
                second_color_pos = np.where(input_array == second_color)
                second_color_idx = (second_color_pos[0][0], second_color_pos[1][0])
                if color_idx < second_color_idx:
                  second_color = color

            output_grid[:, :] = first_color
            output_grid[1, 1] = second_color  # Overwrite bottom-right if a second color exists

    return output_grid.tolist()