"""
The transformation rule is a reflection or mirroring of the grid across a central vertical axis. The right side is mirrored to the left, and the bottom on the top.
"""

import numpy as np

def find_colored_line(grid, colors):
    # Find the vertical line with specified colors
    rows, cols = grid.shape
    for c in reversed(range(cols)):  # Iterate from right to left
        col_pixels = []
        for r in range(rows):
            if grid[r,c] in colors:
                col_pixels.append((r,c, grid[r,c]))
        if len(col_pixels) > 0:
            return col_pixels
    return []

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the right side marron and green vertical line
    right_colors = [9,3]
    right_line = find_colored_line(input_grid, right_colors)
   
    # Find the left side red and yellow vertical line
    left_colors = [2,4]
    left_line = find_colored_line(input_grid, left_colors)
    
    #Flip vertically top with down
    for r_row, r_col, r_color in right_line:
            output_grid[rows - 1 - r_row, r_col] = r_color

    # Mirror the right line to the left side.
    for r_row, r_col, r_color in right_line:
            output_grid[r_row, cols-1-r_col] = r_color
    
    # Mirror the left pixels to the correct location.
    for l_row, l_col, l_color in left_line:
        output_grid[rows-1 - l_row,l_col] = l_color
        output_grid[l_row, cols-1 -l_col] = l_color

    
    return output_grid