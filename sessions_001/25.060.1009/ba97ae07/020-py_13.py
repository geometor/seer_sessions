"""
The transformation identifies a blue vertical line and two distinct orange horizontal lines. The input grid is transformed *only* if all the following conditions are met:

1.  A blue vertical line exists (length > 1).
2.  Exactly two distinct orange horizontal lines exist (length > 1).
3.  Both of the orange horizontal lines intersect the blue vertical line.
4. The intersecting pixel is orange.

If all conditions are true, the pixel at the intersection of the blue line and the *lower* of the two orange horizontal lines changes from orange to blue. All other pixels remain unchanged. If any condition is false, the output grid is identical to the input grid.
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find a vertical line of the specified color.
    rows, cols = grid.shape
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] == color:
                # Check if it's a vertical line
                line_length = 0
                for i in range(r, rows):
                    if grid[i, c] == color:
                        line_length += 1
                    else:
                        break
                if line_length > 1: #consider it is a line if lengh > 1
                    return c, r, line_length #return col, start_row, length
    return None, None, None

def find_horizontal_lines(grid, color):
    # Find all horizontal lines of the specified color.
    rows, cols = grid.shape
    lines = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                # Check if it's a horizontal line
                line_length = 0
                for j in range(c, cols):
                    if grid[r, j] == color:
                        line_length += 1
                    else:
                        break

                if line_length > 1:
                    lines.append((r, c, line_length))
                    c += line_length # Skip the rest of this line
    return lines

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find the vertical blue line
    blue_col, blue_start_row, blue_length = find_vertical_line(input_grid, 1)

    # Find all horizontal orange lines
    orange_lines = find_horizontal_lines(input_grid, 7)

    # Check if there are exactly two orange lines and a blue vertical line
    if blue_col is not None and len(orange_lines) == 2:
        # Determine the lower orange line
        orange_lines.sort()  # Sort by row (the first element of the tuple)
        lower_orange_row, _, _ = orange_lines[1]

        # Check for intersection with both lines
        intersects_both = True
        for orange_row, orange_start_col, orange_length in orange_lines:
             if not (blue_start_row <= orange_row < blue_start_row + blue_length and orange_start_col <= blue_col < orange_start_col + orange_length):
                intersects_both = False
                break

        #change color if condition is met
        if intersects_both:
             if output_grid[lower_orange_row, blue_col] == 7:
                output_grid[lower_orange_row, blue_col] = 1

    return output_grid