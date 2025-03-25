"""
The transformation extracts the upper region of the input grid (above the yellow line), and replaces all non-zero values with '3' (green), retaining only the '0's in their original positions. The lower section of the input grid (below the yellow line) has no bearing on the output.
"""

import numpy as np

def transform(input_grid):
    # Find the row index of the separator line (all '4's).
    separator_row_index = -1
    for i, row in enumerate(input_grid):
        if all(pixel == 4 for pixel in row):
            separator_row_index = i
            break

    # If no separator line is found, return an appropriate message or handle the case.
    if separator_row_index == -1:
        return "No separator line found."

    # Define the upper region of the input grid.
    upper_region = input_grid[:separator_row_index]

    # Create the output grid with the same dimensions as the upper region, filled with '3's.
    output_grid = np.full_like(upper_region, 3)

    # Iterate through the upper region and copy '0's to the output grid, and replace others with '3'.
    for i in range(upper_region.shape[0]):
        for j in range(upper_region.shape[1]):
            if upper_region[i, j] == 0:
                output_grid[i, j] = 0  # Keep 0
            # else:  # implicitly already 3, no action needed
            #     output_grid[i,j] = 3

    return output_grid