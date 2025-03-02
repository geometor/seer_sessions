"""
The transformation rule is as follows:
1. Identify the blue (1) vertical line in the input grid.
2. Translate Color: Change the color of blue to azure (8). All other colors become white (0).
3. Compress: Create an output grid that is 5 pixels tall and 3 pixels wide.
4. Draw Segment: Represent the vertical blue line as an azure segment on the first row. The segment starts at column 1 and ends at column 2.
5. Fill Remaining: Fill all other cells of the output grid with white (0).
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find the column index where the vertical line of the specified color exists.
    rows, cols = grid.shape
    for j in range(cols):
        is_line = True
        for i in range(rows):
            if grid[i, j] != color:
                is_line = False
                break
        if is_line:
            return j
    return -1

def transform(input_grid):
    # Initialize output_grid with white (0).
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, 3), dtype=int)

    # Find the vertical blue (1) line.
    blue_line_col = find_vertical_line(input_grid, 1)

    # If a blue line is found, represent it as an azure segment in the output.
    if blue_line_col != -1:
        output_grid[0, 1] = 8
        output_grid[0, 2] = 8

    return output_grid