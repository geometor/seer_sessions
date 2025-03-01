"""
1.  **Examine** the input grid, noting the positions of blue (1) and white (0) pixels.
2.  **Count** the number of blue pixels.
3.  **Identify** the x-coordinates of the left-most and right-most blue pixels.
4.  **Determine** the height of the output grid. The height is equal to the number of blue pixels if there is more than one. Otherwise, it is 1.
5.  **Create** the output grid with the same width as the input grid and the calculated height.
6.  **Fill** a rectangular region in the output grid with blue pixels. The rectangle spans from the x-coordinate of the left-most blue pixel to the x-coordinate of the right-most blue pixel, with a height equal to the calculated output height.
7.  **Copy** all white pixels from the input grid to the output grid, preserving their original row and column positions.
"""

import numpy as np

def get_blue_pixels(grid):
    # return list of (x,y) coordinates of blue pixels
    blue_pixels = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y,x] == 1:
                blue_pixels.append((x,y))
    return blue_pixels

def get_white_pixels(grid):
    # return a list of (x,y) coordinates for all white pixels
    white_pixels = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 0:
                white_pixels.append((x, y))
    return white_pixels

def transform(input_grid):
    # get list of blue pixels
    blue_pixels = get_blue_pixels(input_grid)
    
    # count blue pixels
    num_blue = len(blue_pixels)

    # find x coordinates of left-most and right-most
    if (len(blue_pixels) > 0):
        xs = [p[0] for p in blue_pixels]
        x_min = min(xs)
        x_max = max(xs)
        num_intermediate = x_max - x_min + 1 # Not directly used, but kept for potential future use
    else:
       x_min = 0
       x_max = 0
       num_intermediate = 0

    # height of output
    output_height = num_blue if num_blue > 1 else 1

    # create output grid
    output_grid = np.zeros((output_height, input_grid.shape[1]), dtype=int)

    # fill rectangular region with blue
    if (len(blue_pixels) > 0):
      for y in range(output_height):
          for x in range(x_min, x_max + 1):
              output_grid[y,x] = 1

    # copy ALL white pixels, preserving position
    white_pixels = get_white_pixels(input_grid)
    for x, y in white_pixels:
        if y < output_grid.shape[0]:  # Ensure we don't write out of bounds
             output_grid[y, x] = 0

    return output_grid