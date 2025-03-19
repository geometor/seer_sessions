"""
The transformation rule is as follows:
1. Identify the non-zero pixel in the input grid.
2. Keep the identified non-zero pixel in the same position in the output grid.
3. Create a copy of the non-zero pixel and place it one position to the right of the original in the output grid.
4. Create a copy of the non-zero pixel and place it one position below the original in the output grid.
5. All other pixels should remain 0.
"""

import numpy as np

def find_non_zero_pixel(grid):
    # Iterate through the grid to find the non-zero pixel.
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize the output grid with the same dimensions and values as the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of the non-zero pixel.
    non_zero_coords = find_non_zero_pixel(input_grid)

    if non_zero_coords:
        i, j = non_zero_coords
        value = input_grid[i, j]

        # Replicate the non-zero pixel to the right and below.
        if j + 1 < output_grid.shape[1]:
            output_grid[i, j + 1] = value
        if i + 1 < output_grid.shape[0]:
            output_grid[i + 1, j] = value

    return output_grid