"""
1.  **Identify Green Lines:** Locate all horizontal and vertical lines composed of two or more contiguous green (3) pixels in the input grid.

2.  **Endpoint Evaluation:** For the first and last pixels of each green line (endpoints):
    *   If an endpoint has two *or more* adjacent white pixels (up, down, left, or right), replace it with azure (8).
    *   If an endpoint has only *one* adjacent white pixel, replace with azure if and only if there is at least one green pixel adjacent to this end point.

3.  **Interior Pixel Evaluation:** For all other pixels within each green line (not the first and last pixels):
    *    If a green pixel has *at least one* adjacent white pixel (up, down, left, or right), replace it with azure (8).

4.  **Copy Unmodified Pixels:** Any pixel that is not green, or does not meet the above replacement criteria within a green line, is copied directly from the input grid to the output grid.
"""

import numpy as np

def count_adjacent_white_pixels(grid, row, col):
    """Counts the number of white (0) pixels adjacent to a given cell."""
    count = 0
    rows, cols = grid.shape
    # Check up
    if row > 0 and grid[row - 1, col] == 0:
        count += 1
    # Check down
    if row < rows - 1 and grid[row + 1, col] == 0:
        count += 1
    # Check left
    if col > 0 and grid[row, col - 1] == 0:
        count += 1
    # Check right
    if col < cols - 1 and grid[row, col + 1] == 0:
        count += 1
    return count

def get_green_lines(grid):
    """Identifies horizontal and vertical lines of green pixels."""
    rows, cols = grid.shape
    green_lines = []

    # Check for horizontal lines
    for r in range(rows):
        current_line = []
        for c in range(cols):
            if grid[r, c] == 3:
                current_line.append((r, c))
            else:
                if len(current_line) > 1:
                    green_lines.append(current_line)
                current_line = []
        if len(current_line) > 1:
            green_lines.append(current_line)

    # Check for vertical lines
    for c in range(cols):
        current_line = []
        for r in range(rows):
            if grid[r, c] == 3:
                current_line.append((r, c))
            else:
                if len(current_line) > 1:
                    green_lines.append(current_line)
                current_line = []
        if len(current_line) > 1:
            green_lines.append(current_line)

    return green_lines

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get green lines
    green_lines = get_green_lines(input_grid)

    # Iterate through each green line
    for line in green_lines:
        # Process the line ends
        first_r, first_c = line[0]
        last_r, last_c = line[-1]

        # Check if endpoints have two or more adjacent white pixels
        if count_adjacent_white_pixels(input_grid, first_r, first_c) >= 2:
            output_grid[first_r, first_c] = 8
        elif count_adjacent_white_pixels(input_grid, first_r, first_c) == 1:
            #check for horizontal line
            if first_r == last_r and len(line)>1:
                output_grid[first_r, first_c] = 8
            #check for vertical line
            if first_c == last_c and len(line)>1:
                output_grid[first_r, first_c] = 8

        if count_adjacent_white_pixels(input_grid, last_r, last_c) >= 2:
            output_grid[last_r, last_c] = 8
        elif count_adjacent_white_pixels(input_grid, last_r, last_c) == 1:
             #check for horizontal line
            if first_r == last_r and len(line)>1:
                output_grid[last_r, last_c] = 8
             #check for vertical line
            if first_c == last_c and len(line)>1:
                output_grid[last_r, last_c] = 8

        # Iterate through interior green pixels in line
        for i in range(1, len(line) - 1):
            r, c = line[i]
            if count_adjacent_white_pixels(input_grid, r, c) >= 1:
                output_grid[r, c] = 8

    return output_grid