"""
1.  **Identify Green Pixels:** Locate all green (3) pixels in the input grid.

2.  **Pixel Evaluation:** For each Green Pixel
    *   If a green pixel has *at least one* adjacent white pixel (up, down, left, or right), replace it with azure (8).
    *   If a green pixel does *not* have at least one adjacent white pixel (up, down, left or right) then, if the pixel is part of a horizontal or vertical line of 2 or more, and it is a *line end* (first or last pixel) replace with an azure pixel.

3.  **Copy Unmodified Pixels:** Any pixel that is not green, or does not meet the above replacement criteria, is copied directly from the input grid to the output grid.
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

def is_line_end(line, r, c):
    """Checks if a pixel is at the end of a green line."""
    return (r, c) == line[0] or (r, c) == line[-1]
    

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get green lines
    green_lines = get_green_lines(input_grid)
    all_green_pixels = []
    for line in green_lines:
        all_green_pixels.extend(line)


    # Iterate over all green pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 3:
                # If the green pixel has at least one white neighbor change to azure
                if count_adjacent_white_pixels(input_grid, r, c) >= 1:
                    output_grid[r,c] = 8
                # if not, check if its a line-end
                else:
                    is_end = False
                    for line in green_lines:
                         if is_line_end(line, r, c):
                            is_end = True
                            break
                    if is_end:
                        output_grid[r,c] = 8
    return output_grid