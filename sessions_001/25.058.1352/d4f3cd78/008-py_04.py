"""
1. Identify the Hollow Square: Locate the hollow square object composed of gray pixels.
2. Fill the Square: Fill the interior region of the identified hollow square with azure pixels.
3. Determine the Modification Region: Note the start and end columns of the hollow gray square
4. Modify Last Two Rows: Within the last two rows of the grid, change the color of any white pixels to azure, *but only within the modification region determined in the previous step*.
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

    # Modify the last two rows within the square's column span
    if top_left and bottom_right:
        start_col = top_left[1]
        end_col = bottom_right[1]
        for r in range(rows - 2, rows):
            for c in range(start_col, end_col + 1):  # Inclusive range
                if output_grid[r, c] == 0:
                    output_grid[r, c] = 8

    return output_grid