"""
1.  **Identify the non-zero color:** Scan the input grid to find the single color value that is not zero.
2.  **Count non-zero color in each row:** For each row, determine how many instances of identified color exists.
3.  **Construct the output:** Create a new 1-dimensional array. Its color should be the same as the non-zero color that identified in the input, and the size equal to the number of instances of that color.
"""

import numpy as np

def transform(input_grid):
    # Find the non-zero color
    non_zero_colors = input_grid[input_grid != 0]
    if non_zero_colors.size == 0:  # Handle the case where the input is all zeros
        return np.array([])
    non_zero_color = non_zero_colors[0]

    # Count the total occurrences of the non-zero color
    count = np.sum(input_grid == non_zero_color)

    # Create the output grid
    output_grid = np.full((1, count), non_zero_color)

    return output_grid