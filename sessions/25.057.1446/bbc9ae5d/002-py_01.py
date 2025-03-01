"""
1.  **Examine** the input grid, noting its width and the positions of blue (1) and white (0) pixels.
2.  **Count** the number of blue pixels.
3.  **Identify** the x-coordinates of the left-most and right-most blue pixels. Calculate the number of "intermediate" pixels - the count of pixels between the left-most and right-most blue pixel, inclusive.
4.  **Determine** the height of the output grid. The height is equal to the sum of number of blue pixels and number of "intermediate" pixels.
5.  **Create** the output grid with the same width as the input grid and calculated height.
6.  **Fill** a rectangular region in the output grid with blue pixels. The rectangle starts at the top of the grid, spans from x-coordinate of left-most blue pixel to x-coordinate of the right-most blue pixel, with height equal to the calculated output height.
7.  **Copy** the white pixels from the input grid to the output grid, preserving their relative positions. i.e. output_grid[0, x] = input_grid[0,x] for all x where input_grid[0, x] is white.
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
        num_intermediate = x_max - x_min + 1
    else:
       x_min = 0
       x_max = 0
       num_intermediate = 0

    # height of output
    output_height = num_blue + max(0, num_intermediate - 1) # subtract one since blue pixels is inclusive

    # create output grid
    output_grid = np.zeros((output_height, input_grid.shape[1]), dtype=int)

    # fill rectangular region with blue
    if (len(blue_pixels) > 0):
      for y in range(output_height):
          for x in range(x_min, x_max + 1):
              output_grid[y,x] = 1

    # copy white pixels, preserving position
    for x in range(input_grid.shape[1]):
        if input_grid[0,x] == 0:
            output_grid[0,x] = 0
    
    return output_grid