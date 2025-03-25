"""
The transformation rule is a conditional overlay operation. It identifies two input grids, Grid A and Grid B.
It locates a horizontal line of color 4 (yellow) in Grid B. Using this line as a reference, it overlays a pattern 
onto a 4x4 output grid initialized with color 0 (white). The overlay changes cells to color 3 (green) based on 
the presence of color 1 (blue) in Grid A at corresponding positions within the row region defined by the yellow line
in Grid B.
"""

import numpy as np

def find_yellow_row(grid_b):
    # Find the row index in grid_b that consists entirely of 4s.
    for i, row in enumerate(grid_b):
        if all(cell == 4 for cell in row):
            return i
    return None

def transform(input_grid):
    # Split the input into two grids, Grid A and Grid B.
    grid_a = input_grid[:len(input_grid) // 2]
    grid_b = input_grid[len(input_grid) // 2:]

    # Find the row index of the yellow line in Grid B.
    yellow_row_index = find_yellow_row(grid_b)

    # Initialize the output grid as a 4x4 grid filled with 0s.
    output_grid = np.zeros((4, 4), dtype=int)
    
    grid_a_rows = len(grid_a)
    grid_a_cols = len(grid_a[0])


    # Perform the conditional overlay.
    if yellow_row_index is not None:
        for r in range(4):
            for c in range(4):
                grid_b_row = yellow_row_index -1 + r
                grid_b_col = c
                
                if 0 <= grid_b_row < grid_a_rows and 0 <= grid_b_col < grid_a_cols:
                    if grid_b[grid_b_row][grid_b_col] == 4 and (grid_a[grid_b_row][grid_b_col] == 1 ):
                        output_grid[r][c] = 3
                    
    return output_grid