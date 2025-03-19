"""
1. Scan the input grid row by row, from top to bottom and left to right.
2. Identify and extract all non-zero (colored) pixels.
3. Maintain the original order of discovery of these pixels.
4. Create 3 x 3 output.
5. Place the non-zero pixels into the output grid sequentially, from top left, following row major order, and filling all 3x3 spaces. If there aren't enough non-zero values to fill the output grid, use 0's.
6. if there are too many non-zero values, then ignore the ones that don't fit.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)
    
    # extract non-zero pixels
    non_zero_pixels = []
    for row in input_grid:
        for pixel in row:
            if pixel != 0:
                non_zero_pixels.append(pixel)

    # place pixels into output grid
    k = 0
    for i in range(3):
        for j in range(3):
            if k < len(non_zero_pixels):
              output_grid[i,j] = non_zero_pixels[k]
              k+=1
            else:
              output_grid[i,j] = 0

    return output_grid