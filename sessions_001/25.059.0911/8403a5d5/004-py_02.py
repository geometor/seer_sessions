"""
1.  **Initialization:** Start with the output grid being the same size as the input grid (10x10).

2.  **Seed Location:** Identify the location of the non-zero pixel (the red '2') in the input grid. In this case, it's at row 9, column 1.

3.  **Column Propagation:**
    *   Every other column starting from the seed column alternates 2 to the height of the grid.
    *    The seed column is the second column in the output and every other column from there is all 2s.

4.  **Row Propagation**:
    *   The seed row is the tenth row in the output and every other row from there is 2 where it is not a 5.

5.  **Fill with 5s**: Every other cell that is at the interseaction of the propogated rows and columns becomes 5, two cells away from the initial seed cell and each other.

6.  **Fill Remaining:** Fill all the other cells in output by a value of 0.
"""

import numpy as np

def find_seed(grid):
    # Find the coordinates of the non-zero pixel.
    rows, cols = np.where(grid != 0)
    if len(rows) > 0:
        return rows[0], cols[0]
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Find seed location
    seed_location = find_seed(input_grid)
    if seed_location is None:
      return output_grid
    seed_row, seed_col = seed_location
    seed_value = input_grid[seed_row, seed_col] # should be 2


    # Column Propagation
    for c in range(seed_col, width, 2):
        output_grid[:, c] = seed_value

    # Row Propagation
    for r in range(seed_row, -1, -2):
        output_grid[r, :] = [seed_value if (c+seed_col) % 2 == 0 and c<width else 0 for c in range(width)]

    # make 5s
    for r in range(seed_row, -1, -2):
      for c in range(seed_col, width, 2):
        if (r-2 >= 0 and c+2 <width) and ((r-seed_row)%2==0 and (c-seed_col)%2==0):
          output_grid[r,c] = 5


    return output_grid