"""
1. Identify the Target Color: Find the single, non-zero color (pixel value) present in the input grid. This color represents the "target object".
2. Replace with Zero: Replace all pixels of the target color with 0 (white).
"""

import numpy as np

def _find_target_color(grid):
    # Find all unique colors in the grid.
    unique_colors = np.unique(grid)
    # Filter out 0 (background color) and return the first remaining color.
    for color in unique_colors:
        if color != 0:
            return color
    return 0  # Return 0 if no target color is found (shouldn't happen in these examples)

def transform(input_grid):
    """
    Transforms the input grid by replacing all instances of the single non-zero color with 0.
    """
    # Create a copy of the input grid to modify.
    output_grid = np.copy(input_grid)

    # Find the target color.
    target_color = _find_target_color(input_grid)

    # Replace all instances of the target color with 0.
    output_grid[input_grid == target_color] = 0

    return output_grid