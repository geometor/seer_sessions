"""
1.  **Identify Horizontal Blue Lines:** Examine each row of the input grid to find all sequences of one or more contiguous blue (1) pixels.  These sequences are "Horizontal Blue Lines." Record the row, starting column, and ending column of each.

2.  **Check for Interruptions:** For *each* Horizontal Blue Line, check if there are any non-blue pixels within the span defined by its starting and ending columns (inclusive) on that row. If non-blue pixels are present, the line is considered "interrupted."

3.  **Transform Interrupted Lines:** If a Horizontal Blue Line is "interrupted," replace *all* pixels within that line's span (from its start column to its end column, inclusive) with the color of the *first* non-blue pixel encountered within that span.

4.  **Preserve Other Pixels:** All pixels that are not part of a transformed Horizontal Blue Line should retain their original color.
"""

import numpy as np

def find_horizontal_blue_lines(grid):
    """Finds all horizontal lines of blue pixels and checks for interruptions."""
    blue_lines = []
    for i, row in enumerate(grid):
        start = -1
        for j, pixel in enumerate(row):
            if pixel == 1:
                if start == -1:
                    start = j
            elif start != -1:
                blue_lines.append((i, start, j - 1))
                start = -1
        if start != -1:  # Handle line ending with blue
            blue_lines.append((i, start, len(row) - 1))
    return blue_lines

def is_interrupted(grid, line):
    """Checks if a horizontal line has any non-blue pixels."""
    row, start, end = line
    for j in range(start, end + 1):
        if grid[row, j] != 1:
            return True
    return False

def find_first_interrupting_color(grid, line):
    """Finds the color of the first non-blue pixel in an interrupted line."""
    row, start, end = line
    for j in range(start, end + 1):
        if grid[row, j] != 1:
            return grid[row, j]
    return None  # Should not happen if the line is truly interrupted

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)

    # Find horizontal blue lines
    blue_lines = find_horizontal_blue_lines(grid)

    # Process all blue lines
    for line in blue_lines:
        if is_interrupted(grid, line):
            interrupting_color = find_first_interrupting_color(grid, line)
            row, start, end = line
            for j in range(start, end + 1):
                output_grid[row, j] = interrupting_color

    return output_grid.tolist()