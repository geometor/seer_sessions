"""
1.  **Identify the Pattern:** Extract the 3x3 subgrid from the top-left corner of the input grid. This subgrid will serve as the repeating pattern unit. In this example it is `[[2, 8, 3], [8, 3, 0], [3, 0, 0]]`

2.  **Replicate and Fill:** Replicate this 3x3 pattern across the entire output grid, tiling it horizontally and vertically. Replace all 0s with the value of the pixel to its immediate left.

3. Specifically, iterate through the output grid. For each cell:
    - if the corresponding input x,y coordinates mod 3 match the output x,y coordinate, set the output value to be equal to the input value at the mod 3 coordinate.
    - otherwise, if the cell value is 0 (white), set its value to the color of the cell immediately to its left.
    - If no value to left, look up.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Replicate the 3x3 pattern
    for i in range(height):
        for j in range(width):
            output_grid[i, j] = input_grid[i % 3, j % 3]

    # Fill 0s with the value to the left, or up if on the edge.
    for i in range(height):
        for j in range(width):
            if output_grid[i, j] == 0:
                if j > 0:
                    output_grid[i, j] = output_grid[i, j - 1]
                elif i > 0:
                    output_grid[i,j] = output_grid[i-1,j]

    return output_grid.tolist()