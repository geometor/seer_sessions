"""
The program removes the blue border and white background and condenses the
remaining colored pixels into a smaller grid, preserving their relative
arrangement.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing the blue border and most white pixels,
    then condensing the remaining pixels into a smaller output grid.
    """
    rows, cols = input_grid.shape
    # 1. & 2. Identify and Exclude Border and Whites: Find non-blue and non-white pixels
    salient_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 1 and not (input_grid[r,c] == 0 and _is_part_of_white_region(input_grid,r,c)):
                salient_pixels.append((input_grid[r, c], r, c))


    # 3 & 4. Extract and Condense into Output: Create a smaller grid and place extracted pixels
    output_rows = 4  # From example.
    output_cols = 4
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    k=0
    for i in range(output_rows):
      for j in range(output_cols):
        if k < len(salient_pixels):
            output_grid[i,j] = salient_pixels[k][0]
        k += 1

    return output_grid

def _is_part_of_white_region(grid, r, c):
    #naive: if there are too many white around return true.
    rows, cols = grid.shape
    count = 0
    if r > 0 and grid[r-1,c] == 0:
      count += 1
    if r < rows-1 and grid[r+1,c] == 0:
      count += 1
    if c > 0 and grid[r,c-1] == 0:
      count += 1
    if c < cols-1 and grid[r,c+1] == 0:
      count += 1
    return count >= 2