"""
The transformation rule divides the input grid into two halves: Grid A (top) and Grid B (bottom).
Grid B always has a yellow (4) row at the top (row 0). The output is a 4x4 grid.
If a cell in Grid A is blue (1) at (r_a, c_a), then the output grid has a green (3)
pixel at (3 - r_a + r_b, c_a), where r_b is the index of the yellow row in Grid B (always 0).
The output grid's dimensions are always 4x4.
"""

import numpy as np

def transform(input_grid):
    # Split the input into two grids, Grid A and Grid B.
    grid_a = input_grid[:len(input_grid) // 2]
    grid_b = input_grid[len(input_grid) // 2:]

    # Find the row index of the yellow line in Grid B (always 0).
    yellow_row_index = 0

    # Initialize the output grid as a 4x4 grid filled with 0s.
    output_grid = np.zeros((4, 4), dtype=int)

    # Perform the conditional overlay.
    for r_a in range(len(grid_a)):
        for c_a in range(len(grid_a[0])):
            if grid_a[r_a][c_a] == 1:
                r_o = 3 - r_a + yellow_row_index
                c_o = c_a
                if 0 <= r_o < 4 and 0 <= c_o < 4:
                    output_grid[r_o][c_o] = 3
                    
    return output_grid