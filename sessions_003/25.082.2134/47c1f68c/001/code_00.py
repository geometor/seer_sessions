"""
1.  **Identify the Horizontal Line:** Locate the single, horizontal line of uniform color that spans the entire width of the input grid.
2.  **Note the Horizontal Line's color:** Remember that the horizontal line original color.
3.  **Identify Colored Squares:** Find the colored squares (single cells or small groups of adjacent cells of the same color) located above and below the horizontal line, that DO NOT match the horizontal line's color.
4.  **Replace Square Colors:** Change the color of these identified squares to the color of the horizontal line, *from the input grid*.
5.  **Blank out Horizontal line:** Blank out (fill with '0') the horizontal line.
6.  **Preserve Background:** Ensure all cells with a value of 0 (white) in the input grid remain 0 in the output grid.
"""

import numpy as np

def find_horizontal_line(grid):
    rows, cols = grid.shape
    for r in range(rows):
        first_val = grid[r, 0]
        if first_val == 0:
            continue
        if np.all(grid[r, :] == first_val):
            return r, first_val
    return None, None

def find_colored_squares(grid, horizontal_line_row, horizontal_line_color):
    rows, cols = grid.shape
    squares = []
    for r in range(rows):
        for c in range(cols):
            if r != horizontal_line_row and grid[r,c] != 0 and grid[r,c] != horizontal_line_color:
                squares.append((r, c, grid[r,c]))
    return squares

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # change output pixels

    # Find the horizontal line and its color
    horizontal_line_row, horizontal_line_color = find_horizontal_line(input_grid)

    # find colored sqaures
    squares = find_colored_squares(input_grid, horizontal_line_row, horizontal_line_color)

    # set the squares in the output
    for r, c, old_color in squares:
      output_grid[r,c] = horizontal_line_color

    return output_grid.tolist()