"""
Finds the rightmost occurrence of each of the target colors (1, 2, and 4) within the input grid. 
Creates a 3x3 output grid where each row consists of the target colors found, in the order they appear.
If a target color is not found, 0 (background) is used in its place. If multiple instances
of the same color are found the rightmost takes precedence.
"""

import numpy as np

def get_rightmost_target_colors(input_grid):
    """
    Finds the rightmost occurrence of each target color (1, 2, and 4) in the input grid.
    Returns a list of these color values, maintaining the order they appear in the grid
    """
    target_colors = [1, 2, 4]
    rightmost_values = []
    found_colors = []

    for j in range(input_grid.shape[1] -1, -1, -1):  # Iterate through columns right to left
        for i in range(input_grid.shape[0]):
            color = input_grid[i, j]
            if color in target_colors and color not in found_colors:
                rightmost_values.append(color)
                found_colors.append(color)
    
    #fill in missing colors with 0
    for color in target_colors:
        if color not in found_colors:
          rightmost_values.append(0)

    #ensure the return is only ever 3 colors
    return rightmost_values[:3]

def transform(input_grid):
    # Find rightmost values of target colors, in order
    target_values = get_rightmost_target_colors(input_grid)

    # Construct the 3x3 output grid
    output_grid = np.array([target_values, target_values, target_values])

    return output_grid