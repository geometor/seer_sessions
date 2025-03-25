"""
1.  **Identify Seed Pixels:** Locate all pixels within the input grid that possess non-zero values. These pixels are designated as "seed" pixels.

2.  **Initialize Output Grid:** Create a copy of the input grid to serve as the output grid. Preserve all original seed pixel values.

3.  **Downward Propagation (Precedence):**
    *   Each seed pixel initiates a downward propagation of its color value within its respective column.
    *   This propagation continues until one of the following conditions is met:
        *   The bottom row of the grid is reached.
        *   An obstruction is hit - a non-zero cell is encountered, including
            other seed pixels and cells filled by another downward propigation.

4.  **Rightward Propagation:**
    *   Each seed pixel initiates a rightward propagation of its color value within its respective row.
    *   This propagation continues until one of the following conditions is met:
        *   The rightmost column of the grid is reached.
        *   An obstruction is hit - if the cell directly below is not zero or if
            the cell has already been filled by a previous downward propigation

5.  **Output:** The output grid, now modified by the propagation rules, represents the final transformed grid.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Finds the coordinates of all non-zero pixels in the grid.
    """
    rows, cols = np.where(grid != 0)
    return list(zip(rows, cols))

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # get non-zero pixels
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # if no non-zero pixels, return original grid
    if not nonzero_pixels:
      return output_grid

    # Propagate downwards first (higher precedence)
    for r, c in nonzero_pixels:
        val = input_grid[r,c]
        # Propagate down
        for i in range(r + 1, height):
            if output_grid[i, c] != 0 and (i,c) not in nonzero_pixels: # Check if another downward prop already filled this cell
              break  #stop the downward prop if it hit a filled cell
            output_grid[i, c] = val

    # Propagate rightwards (lower precedence)
    for r, c in nonzero_pixels:
        val = input_grid[r, c]

        # Propagate right
        for j in range(c + 1, width):
          # check if the cell below is not zero, or if this cell was
          # already filled by downwards prop
          if (r+1 < height and output_grid[r+1,j] != 0) or output_grid[r, j] != 0:
            break
          else:
            output_grid[r, j] = val

    return output_grid