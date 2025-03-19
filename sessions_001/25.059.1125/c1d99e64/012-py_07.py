"""
1.  Find the Center: Determine the center column of the input grid.
2.  Identify White Lines: Find all contiguous vertical lines of white (0) pixels that intersect the center column.
3. Find Longest Line: Identify the longest of these vertical white lines. If multiple lines have the same maximal length, it appears that all are changed, so step 3 is included in step 2.
4.  Determine Replacement Color: Find a color from the set [1, 2, 3, 4] that is *not* present in the input grid.
5.  Replace Pixels: Replace all white pixels in the identified longest line(s) that intersect the center column with the determined replacement color.
"""

import numpy as np

def find_center_column(grid):
    """Finds the center column index of the grid."""
    _, cols = grid.shape
    return cols // 2

def find_white_lines(grid, center_col):
    """Finds contiguous vertical lines of white pixels intersecting the center column."""
    rows, _ = grid.shape
    white_lines = []
    in_segment = False
    start_row = -1
    for row in range(rows):
        if grid[row, center_col] == 0:
            if not in_segment:
                in_segment = True
                start_row = row
        elif in_segment:
            in_segment = False
            white_lines.append((start_row, row - 1))
            start_row = -1
    if in_segment:
        white_lines.append((start_row, rows - 1))
    return white_lines

def determine_replacement_color(grid):
    """Finds a color from [1, 2, 3, 4] not present in the input grid."""
    unique_colors = np.unique(grid)
    for color in [1, 2, 3, 4]:
        if color not in unique_colors:
            return color
    return None  # Should not happen in valid cases, as per problem constraints

def transform(input_grid):
    """Transforms the input grid based on the defined rules."""
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the Center
    center_col = find_center_column(output_grid)

    # Identify White Lines
    white_lines = find_white_lines(output_grid, center_col)
    
    # Find longest lines
    if not white_lines:
        return output_grid

    max_length = max(end - start + 1 for start, end in white_lines)
    longest_lines = [(start, end) for start, end in white_lines if end - start + 1 == max_length]


    # Determine Replacement Color
    replacement_color = determine_replacement_color(output_grid)

    # Replace Pixels
    for start_row, end_row in longest_lines:
        for row in range(start_row, end_row + 1):
            output_grid[row, center_col] = replacement_color

    return output_grid