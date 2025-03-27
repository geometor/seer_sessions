"""
1.  **Iterate** through each pixel of the input grid.
2.  **Identify** yellow (4) pixels.
3.  **Conditional Transformation:** For each yellow pixel, examine the 2x2 subgrid for which the pixel is a corner (check all four possible corners - top-left, top-right, bottom-left, bottom-right).
4.  **L-Shape identification:** If exactly three of the four pixels in the 2x2 sub-grid are yellow, change the corner yellow pixel to orange (7).
5.  **Output:** The modified grid is the result.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    def is_yellow(pixel):
        return pixel == 4

    def check_2x2_corner(grid, i, j):
        # check if i,j is the top-left corner of a 2x2 block with three yellows
        if i+1 < grid.shape[0] and j+1 < grid.shape[1]:
            subgrid = grid[i:i+2, j:j+2]
            if np.sum(subgrid == 4) == 3:
                return True
        return False
    
    # change output pixels 
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if is_yellow(output_grid[i,j]):
                # check if current pixel is the corner of a 2x2 L
                if check_2x2_corner(output_grid, i, j):
                    output_grid[i,j] = 7
                elif i > 0 and check_2x2_corner(output_grid, i-1, j):
                    output_grid[i,j] = 7
                elif j > 0 and check_2x2_corner(output_grid, i, j-1):
                    output_grid[i,j] = 7
                elif i > 0 and j > 0 and check_2x2_corner(output_grid, i-1, j-1):
                    output_grid[i,j] = 7
                    
    return output_grid