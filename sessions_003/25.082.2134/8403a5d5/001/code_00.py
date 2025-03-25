"""
Transforms a 10x10 grid by expanding a single colored pixel in the last row into a repeating pattern across all rows. The pattern alternates the original color with grey (5) and black(0) based on the position of the original pixel.
"""

import numpy as np

def find_colored_pixel(grid):
    # Find the non-black pixel in the last row
    last_row = grid[-1]
    for x, color in enumerate(last_row):
        if color != 0:
            return x, color
    return None, None  # Should not happen, based on problem definition

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)

    # Find the colored pixel in the last row
    x_start, color = find_colored_pixel(input_grid)

    # Create and apply the repeating sequence for each row
    for y in range(output_grid.shape[0]):
      for x in range(output_grid.shape[1]):
        if x_start % 2 == 0: # if original color column is even
            if x == x_start:
              output_grid[y,x] = color
            elif x == x_start+1:
              output_grid[y,x] = 5
            elif x == x_start+2:
              output_grid[y, x] = color
            elif (x-x_start) % 3 == 0 and x > x_start:
              output_grid[y, x] = color
            elif (x-x_start-1) % 3 == 0 and x > x_start:
                output_grid[y,x]=5
            elif (x-(x_start+2))% 3 ==0 and x > x_start+2:
              output_grid[y,x] = color
            elif (x_start - x) % 3 ==0 and x < x_start:
                output_grid[y, x] = color
            else:
                output_grid[y,x] = 0
        else: # if original color column is odd
            if x == x_start:
              output_grid[y,x] = color
            elif x == x_start-1:
              output_grid[y,x] = 5
            elif x == x_start-2:
              output_grid[y,x] = color
            elif (x-x_start) % 3 == 0 and x < x_start:
              output_grid[y, x] = color
            elif (x_start - x-1) % 3 == 0 and x < x_start:
                output_grid[y,x]=5
            elif (x-x_start+2)% 3 ==0 and x < x_start-2:
                output_grid[y, x] = color
            elif (x_start - x) % 3 ==0 and x > x_start:
                output_grid[y, x] = color

            else:
                output_grid[y,x] = 0


    return output_grid