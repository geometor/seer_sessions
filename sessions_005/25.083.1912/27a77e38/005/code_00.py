"""
Copies the input grid to the output, then changes the centermost pixel on the
bottom row to the color of the pixel directly above it, iterating upwards
until a non-black (non-zero) pixel is found.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = input_grid.copy()

    # Locate Center Column, handling even width
    center_col = width // 2

    # Find Target Pixel on bottom row
    target_row = height - 1
    target_col = center_col

    # Find Replacement Color by searching upwards in the same column
    replacement_color = 0  # Default to black if no other color is found
    for r in range(target_row - 1, -1, -1):  # Iterate upwards from row above target
        if input_grid[r, target_col] != 0:
            replacement_color = input_grid[r, target_col]
            break

    # Change target pixel color
    output_grid[target_row, target_col] = replacement_color

    return output_grid.tolist()