"""
Replaces specific colors in the input grid based on the observed examples.
The transformation identifies replaceable colors and changes them to a
designated color, while leaving other colors unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing specific colors.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Determine replaceable colors and their replacements based on the input
    replaceable_colors = []
    replacements = []

    if 2 in input_grid and 3 not in output_grid and (input_grid==2).sum() > 0 and (output_grid ==2 ).sum() == 0:
        replaceable_colors.append(2)
        replacements.append(3)
    if 4 in input_grid and (input_grid==4).sum() > 0 and (output_grid==4).sum() == 0 :
        replaceable_colors.append(4)
        replacements.append(3)
    if 4 in input_grid and 6 in output_grid and (input_grid == 4).sum() > 0 and (output_grid == 4).sum() == 0 :
      replaceable_colors.append(4)
      replacements.append(6)
    if 6 in input_grid and 0 in output_grid and (input_grid == 6).sum() > 0 and (output_grid == 6).sum() == 0 :
      replaceable_colors.append(6)
      replacements.append(0)

    if 0 in input_grid and 6 in output_grid:
      replaceable_colors.append(0)
      replacements.append(6)

    # Replace colors
    for r in range(rows):
        for c in range(cols):
            for i, color in enumerate(replaceable_colors):
                if output_grid[r, c] == color:
                    output_grid[r, c] = replacements[i]

    return output_grid