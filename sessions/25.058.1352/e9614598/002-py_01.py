"""
1.  **Identify Blue Pixels:** Locate all pixels with the value '1' (blue) in the input grid.
2.  **Determine Cross Center.**: In the examples given, the center of the cross made by 3 (green) is either
    *   the center point between two 1s (blue). Example 1
    *   using a 1 (blue) as an endpoint. Example 2

3.  **Construct Green Cross:** If the center of cross is existing blue, then
   add four green (3) around the center of blue pixels in a plus-sign (+) configuration:
    *   One green pixel directly above the determined center.
    *   One green pixel directly below the determined center.
    *   One green pixel directly to the left of the determined center.
    *   One green pixel directly to the right of the determined center.
4.  **Output Grid:** Create an output grid identical to the input grid. Replace the appropriate cells, using the position of the green crosses, by the value '3'. Retain other cells like 1.
"""

import numpy as np

def get_blue_pixels(grid):
    # Find coordinates of all blue (1) pixels
    blue_pixels = []
    for r_idx, row in enumerate(grid):
        for c_idx, cell in enumerate(row):
            if cell == 1:
                blue_pixels.append((r_idx, c_idx))
    return blue_pixels

def construct_cross(grid, blue_pixels):
    #create green cross pattern

    output_grid = np.copy(grid)
    if not blue_pixels:
        return output_grid

    for blue_pixel in blue_pixels:

        row, col = blue_pixel
        # Construct green cross around the blue pixel
        if row > 0:
            output_grid[row - 1, col] = 3  # Above
        if row < len(grid) - 1:
            output_grid[row + 1, col] = 3  # Below
        if col > 0:
            output_grid[row, col - 1] = 3  # Left
        if col < len(grid[0]) - 1:
            output_grid[row, col + 1] = 3  # Right

    return output_grid

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)

    # Find coordinates of all blue (1) pixels
    blue_pixels = get_blue_pixels(input_grid)

    # Construct cross using a function
    output_grid = construct_cross(input_grid, blue_pixels)

    return output_grid.tolist()