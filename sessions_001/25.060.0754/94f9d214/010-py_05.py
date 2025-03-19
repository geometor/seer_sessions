"""
The transformation identifies 2x2 squares of the same color in the input grid.
If a 2x2 square of the same color is found, the corresponding cell in the output grid is colored red (2).
All other cells in the output grid are white (0). The output grid is 1/4 the size of the input grid.
Specifically, it takes color from the top-left corner of 2x2 in input and puts to top left corner of output, for example:

Input Grid:
3 3 3 3     2x2 of 3s
0 3 3 0
0 0 3 3
3 0 0 0
0 0 0 1
0 0 0 1     2x2 of 1s
0 1 0 0
1 0 0 1

Output Grid:
0 0 0 0
2 0 0 0  <- Top-left of the 2x2 of 3s is red
2 0 0 0  <- Top-left of the 2x2 of 1s is red
0 2 2 0
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows // 2, cols // 2), dtype=int)

    # Iterate through the input grid, checking for 2x2 squares.
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Extract 2x2 subgrid
            subgrid = input_grid[i:i+2, j:j+2]

            # Check if all elements in the subgrid are the same
            if np.all(subgrid == subgrid[0, 0]):
                # Map the position to the output grid
                output_row = i // 2
                output_col = j // 2
                if output_row < output_grid.shape[0] and output_col < output_grid.shape[1]:
                  output_grid[output_row, output_col] = 2

    return output_grid.tolist()