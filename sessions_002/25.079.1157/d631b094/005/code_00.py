"""
1.  **Identify Target Color:** Examine the input grid and determine the single non-black color. This is the "target color".
2.  **Count Target Pixels:** Count the number of pixels in the input grid that have the target color.
3.  **Construct Output Grid:** Create a new grid with a height of 1 and a width equal to the count of target pixels from step 2.
4.  **Fill Output Grid:** Fill every cell of the output grid with the target color.
"""

import numpy as np

def get_target_color(grid):
    # Find unique colors in the grid, excluding black (0)
    unique_colors = np.unique(grid)
    target_colors = unique_colors[unique_colors != 0]
    # Return the first non-black color, assumes there's only one
    if len(target_colors) > 0:
       return target_colors[0]
    else:
        return 0

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Target Color
    target_color = get_target_color(input_grid)
    if target_color == 0: return [] # Handle cases with no target color.

    # 2. Count Target Pixels
    target_color_count = np.count_nonzero(input_grid == target_color)

    # 3. Construct Output Grid
    output_grid = np.full((1, target_color_count), target_color)

    # 4. Fill Output Grid (already done in construction)

    return output_grid.tolist()