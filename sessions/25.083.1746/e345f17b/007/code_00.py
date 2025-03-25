"""
1.  **Input and Output Grids:** The input is a grid of colors (represented by integers 0-9). The output grid has the same height as the input grid. The output grid's width is half the width of the input grid (using integer division, effectively rounding down).

2.  **2x2 Region Iteration:** The input grid is processed by examining non-overlapping 2x2 regions. Start at the top-left corner (0,0). Move two steps to the right for each successive region in a row. Move one step down for each successive row.

3. **Output Mapping** For *each* row in the input grid, and for *every two* columns, map the corresponding input area to *one* column in the output grid.

4.  **Magenta Check:** Within each 2x2 region of the input, check for the presence of magenta (color 6).

5.  **Output Generation:**
    *   If the 2x2 region *contains* magenta, place a yellow pixel (color 4) in the corresponding cell of the output grid. The output cell's row index is the same as the 2x2 region's starting row index. The output cell's column index is the 2x2 region's starting column index divided by 2 (integer division).
    *   If the 2x2 region does *not contain* magenta, place a white pixel (color 0) in the corresponding cell of the output grid. The output cell's location in the grid is determined by the process in Step 3.
"""

import numpy as np

def contains_magenta(two_by_two):
    """Checks if a 2x2 region contains magenta (6)."""
    return np.any(two_by_two == 6)

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height
    output_width = input_width // 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # iterate over 2x2 regions in the input
    for row in range(input_height):  # Step by 1 for rows
        for col in range(0, input_width, 2):  # Step by 2 for columns
            # extract 2x2 region, limited by input boundaries.
            two_by_two = []
            for i in range(2):
                row_values = []
                for j in range(2):
                    if row+i < input_height and col +j < input_width:
                        row_values.append(input_grid[row + i][col + j])
                    else:
                        row_values.append(0)  # Use 0 for padding
                two_by_two.append(row_values)

            two_by_two = np.array(two_by_two)

            # check for magenta
            has_magenta = contains_magenta(two_by_two)

            # place yellow or white
            output_col = col // 2
            if has_magenta:
                output_grid[row, output_col] = 4
            else:
                output_grid[row, output_col] = 0

    return output_grid