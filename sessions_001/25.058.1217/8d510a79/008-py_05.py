"""
1.  **Identify the Separator:** Find the single horizontal line composed entirely of gray (5) pixels. This line divides the grid into an "above" section and a "below" section.

2.  **Process Above Separator:** For each blue (1) or red (2) pixel located *above* the separator line:
    *   Replicate the color of that pixel downwards, in the same column, until the next cell above the separator is reached, or until a non-white cell is encountered.

3.  **Process Below Separator:** For each blue (1) or red (2) pixel located *below* the separator line:
    *   Replicate the color of that pixel upwards, in the same column, until the next cell below the separator is reached, or until a non-white cell is encountered.
4. White(0) pixels remain unchanged.
5. Gray(5) horizontal line remains unchanged and serves as a boundary.
"""

import numpy as np

def find_separator_row(grid):
    # Iterate through rows to find the row consisting entirely of gray (5) pixels
    for i, row in enumerate(grid):
        if np.all(row == 5):
            return i
    return -1  # Separator not found

def extend_pixel_to_separator(grid, row, col, separator_row):
    # Extend the pixel vertically to the separator or the next non-white cell
    rows, cols = grid.shape
    color = grid[row, col]

    if row < separator_row:  # Extend downwards
        for next_row in range(row + 1, separator_row):
            if grid[next_row, col] == 0:
                grid[next_row, col] = color
            else:
                break #stop at non-white
    elif row > separator_row:  # Extend upwards
        for next_row in range(row - 1, separator_row, -1):
            if grid[next_row, col] == 0:
                grid[next_row, col] = color
            else:
                break #stop at non-white

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the separator row
    separator_row = find_separator_row(output_grid)
    if separator_row == -1:
        return output_grid  # No separator, return input as is

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Process blue (1) and red (2) pixels
            if output_grid[r, c] == 1 or output_grid[r, c] == 2:
                if r != separator_row:  #skip if the pixel in on separator row
                    # Extend towards separator
                    extend_pixel_to_separator(output_grid, r, c, separator_row)

    return output_grid