"""
Transforms an input grid into an output grid by identifying horizontal blue lines, extracting corner pixels from the regions defined by these lines, and arranging these corner pixels in the output grid. The output grid's rows are constructed based on the non-zero corner values.
"""

import numpy as np

def find_blue_lines(grid):
    """Finds the row indices of all horizontal blue lines (all pixels are 1)."""
    blue_lines = []
    for i, row in enumerate(grid):
        if all(pixel == 1 for pixel in row):
            blue_lines.append(i)
    return blue_lines

def get_corner_pixels(grid, region_start, region_end):
    """Gets the corner pixels of a region defined by start and end row indices."""
    height, width = grid.shape
    top_left = grid[region_start, 0] if region_start >= 0 else 0
    top_right = grid[region_start, width - 1] if region_start >= 0 else 0
    bottom_left = grid[region_end - 1, 0] if region_end <= height else 0
    bottom_right = grid[region_end - 1, width - 1] if region_end <= height else 0
    return top_left, top_right, bottom_left, bottom_right

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    blue_line_rows = find_blue_lines(input_grid)
    height, width = input_grid.shape
    output_rows = []

    # Handle the region above the first blue line
    if blue_line_rows:
        top_left, top_right, bottom_left, bottom_right = get_corner_pixels(input_grid, 0, blue_line_rows[0])
        if any([top_left, top_right, bottom_left, bottom_right]):
            output_rows.append([bottom_left, top_left, bottom_right, top_right])
            output_rows.append([bottom_left, bottom_left, top_right, top_right])
    else:  # No blue lines, entire grid is one region
        top_left, top_right, bottom_left, bottom_right = get_corner_pixels(input_grid, 0, height)
        if any([top_left, top_right, bottom_left, bottom_right]):
            output_rows.append([bottom_left, top_left, bottom_right, top_right])
            output_rows.append([bottom_left, bottom_left, top_right, top_right])


    # Handle regions between blue lines
    for i in range(len(blue_line_rows) - 1):
        top_left, top_right, bottom_left, bottom_right = get_corner_pixels(input_grid, blue_line_rows[i] + 1, blue_line_rows[i+1])
        if any([top_left, top_right, bottom_left, bottom_right]):
          output_rows.append([bottom_left, top_left, bottom_right, top_right])
          output_rows.append([bottom_left, bottom_left, top_right, top_right])

    # Handle region below the last blue line
    if len(blue_line_rows) > 0:
        top_left, top_right, bottom_left, bottom_right = get_corner_pixels(input_grid, blue_line_rows[-1] + 1, height)
        if any([top_left, top_right, bottom_left, bottom_right]):
          output_rows.append([bottom_left, top_left, bottom_right, top_right])
          output_rows.append([bottom_left, bottom_left, top_right, top_right])


    output_grid = np.array(output_rows)
    return output_grid.tolist()