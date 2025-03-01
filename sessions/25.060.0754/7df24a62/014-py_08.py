"""
Copies yellow pixels from the input to the output grid. Conditionally creates a 3x4 blue block with a central yellow pixel based on the number and position of yellow pixels in the input.
"""

import numpy as np

def find_yellow_pixels(grid):
    """Finds the coordinates of all yellow (4) pixels in the grid."""
    return np.argwhere(grid == 4)

def create_blue_block(output_grid, center_x, center_y):
    """Creates a 3x4 blue block with a central yellow pixel."""
    for i in range(center_y - 1, center_y + 3):  # Iterate for height of 4
        for j in range(center_x - 1, center_x + 2):  # width of three
            if 0 <= i < output_grid.shape[0] and 0 <= j < output_grid.shape[1]:
                output_grid[i, j] = 1
    # Place yellow pixel at center
    yellow_row = center_y + 1
    yellow_col = center_x
    if 0 <= yellow_row < output_grid.shape[0] and 0 <= yellow_col < output_grid.shape[1]:
        output_grid[yellow_row, yellow_col] = 4

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)
    #height, width = input_grid.shape #not used

    # Copy Yellow Pixels
    yellow_pixels = find_yellow_pixels(input_grid)
    #for y, x in yellow_pixels: # redundant
    # output_grid[y, x] = 4

    # Conditional Blue Block Creation
    if len(yellow_pixels) >= 2:
        # Find yellow pixel positions and sort by row
        yellow_pixels = sorted(yellow_pixels, key=lambda p: p[0])
        min_y = yellow_pixels[0][0]
        max_y = yellow_pixels[-1][0]
        min_x = min(p[1] for p in yellow_pixels)


        # Blue block placement
        if max_y - min_y > 0:
          center_y = min_y - 2
        else:
          center_y = min_y -1

        center_x = min_x
        create_blue_block(output_grid, center_x, center_y)

    return output_grid