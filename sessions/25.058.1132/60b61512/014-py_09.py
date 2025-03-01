"""
1.  **Identify** all horizontal lines of yellow pixels within the input grid.
2.  **Locate** the rightmost yellow pixel of *each* horizontal yellow line.
3.  **Change** the color of *each* identified rightmost yellow pixel to orange (7).
4.  **Preserve** all other pixels as they are in the input grid.
"""

import numpy as np

def find_horizontal_lines(grid, color):
    """Finds all horizontal lines of a given color."""
    lines = []
    for row_idx, row in enumerate(grid):
        current_line = []
        for col_idx, pixel in enumerate(row):
            if pixel == color:
                current_line.append((row_idx, col_idx))
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = []
        if current_line:  # Handle lines that extend to the end of the row
            lines.append(current_line)
    return lines

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all horizontal yellow lines
    yellow_lines = find_horizontal_lines(input_grid, 4)

    # Change the rightmost pixel of each line to orange
    for line in yellow_lines:
        rightmost_pixel = line[-1]
        output_grid[rightmost_pixel[0], rightmost_pixel[1]] = 7

    return output_grid