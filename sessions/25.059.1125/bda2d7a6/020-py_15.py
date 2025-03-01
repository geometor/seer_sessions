"""
1.  **Determine Background:** The background color is the most frequent color in the input grid, *or* the color in the corners.
2.  **Identify Colors to Swap:** Identify the two most frequent colors, excluding the background color. If fewer than two colors remain, do nothing.
3.  **Swap Colors:** Iterate through all pixels of the input grid. If a pixel's color matches the first color to swap, change it to the second color. If it matches the second color, change it to the first.
4.  **Preserve Background:** Do not change pixels that match the background color.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    # Check corners first, then most frequent
    corners = [grid[0, 0], grid[0, -1], grid[-1, 0], grid[-1, -1]]
    corner_counts = Counter(corners)
    most_common_corner = corner_counts.most_common(1)
    if most_common_corner:
        return most_common_corner[0][0]
    
    # else return most frequent overall
    all_colors = grid.flatten().tolist()
    color_counts = Counter(all_colors)
    return color_counts.most_common(1)[0][0]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Determine Background
    background_color = get_background_color(output_grid)

    # Identify Colors to Swap
    color_counts = Counter(output_grid.flatten())
    color_counts.pop(background_color, None)  # Remove background color

    if len(color_counts) < 2:
        return output_grid  # Not enough colors to swap

    most_common_colors = color_counts.most_common(2)
    color1 = most_common_colors[0][0]
    color2 = most_common_colors[1][0]

    # Swap Colors
    for row in range(output_grid.shape[0]):
        for col in range(output_grid.shape[1]):
            if output_grid[row, col] == color1:
                output_grid[row, col] = color2
            elif output_grid[row, col] == color2:
                output_grid[row, col] = color1

    return output_grid