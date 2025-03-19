"""
1.  **Identify Blue Lines:** Find all horizontal lines composed entirely of blue pixels.
2.  **Find Lowest Blue Line:** Among the identified blue lines, select the one with the largest row index (i.e., the lowest one on the grid).
3.  **Downward Fill:** Starting from the row immediately below the lowest blue line, and proceeding downwards, change the color of each pixel in the grid to blue.
4.  **Stopping Condition:** This downward filling stops when a pixel of any color *other than white* is encountered in the current column. If no non-white pixel is found, the filling continues to the bottom of the grid.
"""

import numpy as np

def find_horizontal_lines(grid, color):
    # Find all horizontal lines of a specific color
    rows, cols = grid.shape
    lines = []
    for r in range(rows):
        if all(grid[r, c] == color for c in range(cols)):
            lines.append(r)
    return lines

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find all blue horizontal lines
    blue_lines = find_horizontal_lines(input_grid, 1)

    # If no blue lines are found, return the original grid
    if not blue_lines:
        return output_grid

    # Find the lowest blue line
    lowest_blue_line_row = max(blue_lines)

    # Perform downward fill
    for c in range(cols):
        for r in range(lowest_blue_line_row + 1, rows):
            if input_grid[r, c] != 0:  # Check for non-white pixel
                break  # Stop filling if a non-white pixel is encountered
            output_grid[r, c] = 1  # Fill with blue

    return output_grid