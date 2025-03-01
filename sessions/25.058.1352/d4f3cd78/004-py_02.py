"""
1. Identify a hollow square object formed by gray (5) pixels within the grid.
2. Fill the interior region of the identified square with azure (8) pixels.
3. Locate the last two rows.
4. Change the color value of white(0) into azure(8) in the last two rows.
"""

import numpy as np

def find_hollow_square(grid, square_color=5):
    rows, cols = grid.shape
    top_left = None
    bottom_right = None

    # Find top-left corner
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == square_color:
                top_left = (r, c)
                break
        if top_left:
            break

    # Find bottom-right corner
    if top_left:
        for r in range(rows - 1, -1, -1):
            for c in range(cols - 1, -1, -1):
                if grid[r, c] == square_color:
                    bottom_right = (r, c)
                    break
            if bottom_right:
                break
    return top_left, bottom_right

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the hollow square
    top_left, bottom_right = find_hollow_square(output_grid)

    # Fill the interior of the square with azure (8)
    if top_left and bottom_right:
        for r in range(top_left[0] + 1, bottom_right[0]):
            for c in range(top_left[1] + 1, bottom_right[1]):
                output_grid[r, c] = 8

    # Change '0' to '8' in the last two rows.
    for r in range(rows-2, rows):
        for c in range(cols):
          if output_grid[r,c] == 0:
            output_grid[r,c] = 8
            

    return output_grid