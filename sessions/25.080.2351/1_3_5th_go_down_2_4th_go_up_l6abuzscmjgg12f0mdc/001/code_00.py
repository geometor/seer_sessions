"""
The transformation rule involves reflecting the non-zero pixels of the input grid across a vertical axis. The non-zero pixels in each row from original matrix form a vertical line.
If there is a zero value in the original matrix, make a value in the same row by selecting the nearest non-zero value of same row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described reflection and filling logic.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
      non_zero_indices = np.where(input_grid[r] != 0)[0]
      if non_zero_indices.size > 0:
        output_grid[r, non_zero_indices[0]:] =  input_grid[r, non_zero_indices]

        for c in range(cols):
          if input_grid[r,c] == 0:
            closest_left = -1
            closest_right = -1

            for i in range(c -1, -1, -1):
              if input_grid[r,i] != 0:
                closest_left = i
                break
            for i in range(c + 1, cols):
              if input_grid[r,i] != 0:
                closest_right = i
                break

            if closest_left != -1 and closest_right != -1:
              if (c - closest_left) <= (closest_right -c):
                output_grid[r,c] = input_grid[r, closest_left]
              else:
                output_grid[r,c] = input_grid[r,closest_right]
            elif closest_left != -1:
              output_grid[r,c] = input_grid[r, closest_left]
            elif closest_right != -1:
              output_grid[r,c] = input_grid[r,closest_right]

      else:
        output_grid[r] = input_grid[r]

    return output_grid.tolist()