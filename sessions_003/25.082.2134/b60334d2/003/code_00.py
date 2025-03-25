"""
Transforms an input grid by copying '5's and generating a checkerboard pattern of '1's and '5's around them. The checkerboard pattern is determined by the sum of row and column indices.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the location of '5's and a checkerboard pattern.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Copy '5's and build checkerboard
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                output_grid[r, c] = 5
            else:
                found_5 = False
                for r_in in range(rows):
                    for c_in in range(cols):
                        if input_grid[r_in,c_in] == 5:
                            found_5 = True
                            break
                    if found_5:
                        break
                if found_5:

                    if (r + c) % 2 == 0:
                        output_grid[r,c] = 1
                    else:
                        output_grid[r,c] = 5
    
    # check if any 5s
    has_5 = False
    for r in range(rows):
      for c in range(cols):
        if output_grid[r,c] == 5:
          has_5 = True
          break
      if has_5:
        break
    
    if not has_5:
      return np.zeros_like(input_grid).tolist()

    # final pass to swap 1s and 5s based on seed
    for r in range(rows):
      for c in range(cols):
        if output_grid[r,c] != 0:          
          if (r + c) % 2 == 0:
              output_grid[r, c] = 5
          else:
              output_grid[r, c] = 1

    return output_grid.tolist()