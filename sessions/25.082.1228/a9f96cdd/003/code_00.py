"""
1.  **Initialization:** Create an output grid of the same size as the input grid, filled with 0 (white).

2.  **Red Pixel Identification:** Locate all pixels with the value 2 (red) in the input grid.

3.  **Transformation based on Red Pixel Location:**
    *   **Corners:**
        *   If the red pixel is at the top-left corner (0, 0), set output[0,0] = 3.
        *   If the red pixel is at the top-right corner (0, cols-1), set output[0,cols-1] = 6.
        *   If the red pixel is at the bottom-left corner (rows-1, 0), set output[rows-1,0] = 8.
        *   If the red pixel is at the bottom-right corner (rows-1, cols-1), set output[rows-1,cols-1] = 7.

    *   **Edges (non-corner):**
        *   If the red pixel is on the top edge (row 0, and not a corner): Set output[1,col-1] to 8, output[1, col+1] to 7.
        *   If the red pixel is on the bottom edge (row rows-1, and not a corner): set output[rows-2, col-1] to 3, and output[rows-2,col+1] = 6.
        *    If the red pixel is on the left edge (column 0, and not a corner): Set output[row-1,1] = 3 and output[row+1,1] = 6.
        *   If the red pixel is on the right edge (column cols-1, and not a corner): Set output[row - 1, cols - 2] to 3, output[row+1, cols-2] to 8, and output[row, cols -2]=0.

4.  **Output:** Return the modified `output_grid`.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 2:
                if i == 0 and j == 0:  # Top Left
                    output_grid[i,j] = 3
                elif i == 0 and j == cols - 1:  # Top Right
                    output_grid[i,j] = 6
                elif i == rows - 1 and j == 0:  # Bottom Left
                    output_grid[i,j] = 8
                elif i == rows - 1 and j == cols - 1:  # Bottom Right
                    output_grid[i,j] = 7
                elif i == 0: # Top edge
                    output_grid[1,j-1] = 8
                    output_grid[1,j+1] = 7
                elif i == rows-1: # Bottom Edge
                    if j > 0:
                      output_grid[rows-2, j-1] = 3
                    if j < cols -1:
                      output_grid[rows-2,j+1] = 6
                elif j == cols-1:  #Right Edge
                    output_grid[i-1, cols-2] = 3
                    output_grid[i+1, cols-2] = 8
                elif j == 0: # Left Edge
                    if i > 0:
                      output_grid[i - 1, 1] = 3
                    if i < rows -1:
                      output_grid[i + 1, 1] = 6
    return output_grid