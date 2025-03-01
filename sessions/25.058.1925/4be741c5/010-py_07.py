"""
The transformation extracts the unique colors from the input grid, preserving their order of first appearance, and arranges them vertically in a new, single-column grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize an empty list to store unique colors
    unique_colors = []

    # Iterate through the input grid row by row, then column by column
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            color = input_grid[i, j]
            # If the color is not already in the list, add it
            if color not in unique_colors:
                unique_colors.append(color)

    # Create a new grid with a single column and height equal to the number of unique colors
    output_grid = np.zeros((len(unique_colors), 1), dtype=int)

    # Populate the output grid with the unique colors
    for i in range(len(unique_colors)):
        output_grid[i, 0] = unique_colors[i]

    return output_grid