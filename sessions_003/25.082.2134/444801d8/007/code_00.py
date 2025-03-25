"""
1.  **Iterate through each row** of the input grid.

2.  **Identify Horizontal Blue Lines:** Within each row, find all contiguous sequences of blue (1) pixels. These are the "Horizontal Blue Lines." Record the row index, starting column, and ending column for each.

3.  **Check for Interruptions on the Same Row:** For each identified Horizontal Blue Line, examine the pixels *on the same row* between the line's starting and ending columns (inclusive). If any pixel in this range is *not* blue (1), the line is considered "interrupted."

4.  **Find the First Interrupting Color (Row-Specific):** If a Horizontal Blue Line is interrupted, find the color of the *first* non-blue pixel encountered *on that specific row*, starting from the beginning of the blue line segment.

5.  **Transform Interrupted Lines (Row-Specific):** If a Horizontal Blue Line on a row is interrupted, replace *all* pixels within that line's span (from its start column to its end column, inclusive) on the *same row* with the color found in step 4.

6.  **Preserve Other Pixels:** All pixels that are not part of a transformed Horizontal Blue Line should retain their original color.
"""

import numpy as np

def find_horizontal_blue_lines(row):
    """Finds all horizontal lines of blue pixels in a single row."""
    blue_lines = []
    start = -1
    for j, pixel in enumerate(row):
        if pixel == 1:
            if start == -1:
                start = j
        elif start != -1:
            blue_lines.append((start, j - 1))
            start = -1
    if start != -1:  # Handle line ending with blue
        blue_lines.append((start, len(row) - 1))
    return blue_lines

def find_first_interrupting_color(row, start, end):
    """Finds the color of the first non-blue pixel in a row segment."""
    for j in range(start, end + 1):
        if row[j] != 1:
            return row[j]
    return None  # Should not happen if the line is truly interrupted

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)

    # Iterate through each row
    for i, row in enumerate(grid):
        # Find horizontal blue lines in the current row
        blue_lines = find_horizontal_blue_lines(row)

        # Process each blue line in the current row
        for start, end in blue_lines:
            # Check for interruptions on the same row
            interrupting_color = find_first_interrupting_color(row, start, end)
            if interrupting_color is not None:  # Line is interrupted
                # Replace pixels with the interrupting color
                for j in range(start, end + 1):
                    output_grid[i, j] = interrupting_color

    return output_grid.tolist()