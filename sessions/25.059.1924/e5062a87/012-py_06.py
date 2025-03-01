"""
Extends colored lines horizontally to grid boundaries or until a different color is encountered.
"""

import numpy as np

def get_background_color(grid):
    # the background color is assumed to be in every example to be white
    return 0

def find_horizontal_lines(grid):
    """Finds all horizontal line segments in a grid."""
    background_color = get_background_color(grid)
    lines = []
    for r_idx, row in enumerate(grid):
        c_idx = 0
        while c_idx < len(row):
            pixel = row[c_idx]
            if pixel != background_color:
                # Start of a potential line segment
                segment = []
                c = c_idx
                while c < len(row) and row[c] == pixel:
                    segment.append((r_idx, c))
                    c += 1
                if len(segment) > 1:  # Consider it a line only if length > 1
                    lines.append(segment)
                c_idx = c  # move the index
            else:
                c_idx += 1
    return lines

def extend_line(grid, line_segment):
    """Extends a single horizontal line segment."""
    background_color = get_background_color(grid)
    output_grid = np.copy(grid)
    row_index = line_segment[0][0]
    line_color = grid[line_segment[0]]

    # Extend to the left
    c_left = line_segment[0][1] - 1
    while c_left >= 0 and output_grid[row_index, c_left] == background_color:
        output_grid[row_index, c_left] = line_color
        c_left -= 1

    # Extend to the right
    c_right = line_segment[-1][1] + 1
    while c_right < output_grid.shape[1] and output_grid[row_index, c_right] == background_color:
        output_grid[row_index, c_right] = line_color
        c_right += 1

    return output_grid

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find all horizontal lines
    lines = find_horizontal_lines(grid)

    # Extend each line
    output_grid = np.copy(grid) # start the output
    for line in lines:
        output_grid = extend_line(output_grid, line) # extend each line

    return output_grid.tolist()