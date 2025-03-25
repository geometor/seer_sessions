"""
1.  **Identify Common Colors:** Find the set of colors present in *both* the input and output grids, excluding 0 (the background color).
2.  **Determine Output Height:** The output height is the number of rows in the input containing any of the common non-zero colors.
3.  **Determine Output Width:** The output width is the number of common colors (excluding 0).
4. **Construct Output Grid:** Create a new grid with the calculated dimensions.
5. **Populate Output Grid:**  For each row in the output grid, fill the entire row with the sorted common colors.
"""

import numpy as np

def get_common_colors(input_grid, output_grid):
    """Finds common non-zero colors between input and output grids."""
    input_colors = set(input_grid.flatten())
    output_colors = set(output_grid.flatten())
    common_colors = sorted(list(input_colors.intersection(output_colors)))
    return [c for c in common_colors if c != 0]

def get_output_height(input_grid, common_colors):
    """Calculates the output height based on rows with common colors."""
    output_height = 0
    for row in input_grid:
        if any(color in common_colors for color in row):
            output_height += 1
    return output_height

def transform(input_grid, output_grid):
    # Identify common colors
    common_colors = get_common_colors(input_grid, output_grid)

    # Determine output width
    output_width = len(common_colors)

    # Determine output height
    output_height = get_output_height(input_grid, common_colors)


    # Construct output grid
    output_grid_result = np.zeros((output_height, output_width), dtype=int)

    # Populate output grid
    for i in range(output_height):
        output_grid_result[i, :] = sorted(common_colors)

    return output_grid_result