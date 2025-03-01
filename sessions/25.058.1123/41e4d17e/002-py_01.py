"""
The transformation identifies blue shapes on an azure background.
The blue shape are outlined with magenta. Also, the a magenta vertical line is added,
based on the y axis mid point of all blue shapes.
"""

import numpy as np

def find_blue_shapes(grid):
    # Find all blue (1) pixels
    blue_pixels = np.argwhere(grid == 1)
    return blue_pixels

def find_y_midpoints(pixels):
    # extract all unique y coordinates
    unique_y = []
    for x,y in pixels:
      if y not in unique_y:
        unique_y.append(y)

    return unique_y

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find blue shapes
    blue_pixels = find_blue_shapes(input_grid)

    # Find y axis of the blue pixels
    y_axis = find_y_midpoints(blue_pixels)

    #add magenta line based on the y position of blue pixels
    for x in range(input_grid.shape[0]):
       for y in y_axis:
        output_grid[x,y] = 6
    # Add magenta (6) around each blue pixel
    for r, c in blue_pixels:
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds and if the neighbor is not blue (to avoid overwriting the shape itself).  Also consider if the neighbor is not already magenta to avoid duplicate placement
            if 0 <= nr < output_grid.shape[0] and 0 <= nc < output_grid.shape[1] and output_grid[nr, nc] != 1 and output_grid[nr,nc] != 6:
                output_grid[nr, nc] = 6


    return output_grid