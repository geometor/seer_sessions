```python
"""
1.  **Grid Dimensions:** The output grid has the same height as the input grid. The output grid's width is calculated as `(input_grid_width + 1) // 2`.

2.  **2x2 Region Iteration:** The input grid is processed by iterating through non-overlapping 2x2 regions.

3.  **Magenta Check:** Within each 2x2 region, check for the presence of magenta (color 6).

4.  **Output Generation - Magenta Found:**
    *   If magenta is found, determine the *last* position of magenta in the 2x2 region by reading left-to-right, top-to-bottom.
    *  Place a yellow pixel (4) in the output grid. The output grid row corresponds to the 2x2 block's row index. The output column is calculated based on the relative column index (0 or 1) of the last magenta pixel.
    
5.  **Output Generation - No Magenta:** If no magenta is found in the 2x2 region, place a white pixel (0) in the corresponding cell of the output grid, using the 2x2 region's top-left corner's row and column indices.
"""

import numpy as np

def get_last_magenta_position(two_by_two):
    """Finds the last position of magenta (6) in a 2x2 region."""
    last_magenta_position = None
    for i in range(2):
        for j in range(2):
            if two_by_two[i, j] == 6:
                last_magenta_position = (i, j)
    return last_magenta_position

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height
    output_width = (input_width + 1) // 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # iterate over 2x2 regions in the input
    for row in range(0, input_height, 1):  # Step by 1 for rows
        for col in range(0, input_width, 2):  # Step by 2 for columns
            # extract 2x2 region, limited by input boundaries.
            two_by_two = []
            for i in range(2):
                row_values = []
                for j in range(2):
                    if row+i < input_height and col +j < input_width:
                        row_values.append(input_grid[row + i][col + j])
                    else:
                        row_values.append(0)
                two_by_two.append(row_values)

            two_by_two = np.array(two_by_two)

            # find the last position of magenta
            last_magenta_pos = get_last_magenta_position(two_by_two)

            # place yellow or white if no magenta exists
            output_col = col // 2
            if last_magenta_pos is not None:
              if last_magenta_pos[1] == 0:
                  output_grid[row][output_col] = 0
              else:
                  output_grid[row][output_col] = 4
            else:
              output_grid[row][output_col] = 0


    return output_grid
```