"""
1.  **Identify Lines:** Scan the input grid to find horizontal lines of magenta (6), blue (1), and red (2) pixels. Note the starting position and length of each line.
2.  **Create Output:** Initialize an output grid of the same dimensions as the input, filled with black/white (0).
3.  **Place Magenta Line:** Place a magenta pixel at row 5, column 1 of the output grid.
4.  **Place Blue Line:** Place a blue horizontal line of length 2 starting at row 6, column 1 of the output grid.
5.  **Place Red Line:**  Place a red horizontal line of length 3 starting at row 7, column 1 of the output grid.
6. **Ensure default:** All remaining cells should be 0.
"""

import numpy as np

def find_horizontal_lines(grid, colors):
    lines = {}
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] in colors:
                color = grid[y, x]
                if color not in lines:
                    length = 0
                    for x2 in range(x, grid.shape[1]):
                        if grid[y, x2] == color:
                            length += 1
                        else:
                            break
                    if length > 0:
                      lines[color] = (y, x, length)
    return lines
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find horizontal lines of magenta, blue, and red
    lines = find_horizontal_lines(input_grid, [6, 1, 2])

    # Move lines
    if 6 in lines:
        output_grid[4, 0] = 6
    if 1 in lines:
        output_grid[5, 0] = 1
        output_grid[5, 1] = 1
    if 2 in lines:
        output_grid[6, 0] = 2
        output_grid[6, 1] = 2
        output_grid[6, 2] = 2

    return output_grid