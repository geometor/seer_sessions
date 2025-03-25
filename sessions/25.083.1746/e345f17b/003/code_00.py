"""
The output grid is constructed by inspecting non-overlapping 2x2 regions of the input grid.
For each 2x2 region, a corresponding cell in the output is determined.
If the 2x2 contains the color magenta (6), check the last position of magenta in the 2x2 region, reading left-to-right and top-to-bottom.
If magenta exists in the 2x2 input, put a yellow in the output grid in a cell corresponding to the relative position of magenta, and a white cell (0) otherwise.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # iterate over 2x2 regions in the input
    for row in range(min(input_height - 1, 4)):
        for col in range(min(input_width - 1, 4)):
            # extract 2x2 region, limited by input boundaries
            two_by_two = []
            for i in range(2):
                row_values = []
                for j in range(2):
                    if row+i < input_height and col +j < input_width:
                        row_values.append(input_grid[row + i][col + j])
                    else:
                        row_values.append(0)  # pad if needed
                two_by_two.append(row_values)
            
            two_by_two = np.array(two_by_two)

            # find the last position of magenta
            magenta_positions = []
            for i in range(2):
                for j in range(2):
                    if two_by_two[i, j] == 6:
                        magenta_positions.append((i, j))

            # place yellow if magenta exists
            if magenta_positions:
                output_grid[row][col] = 4

    return output_grid