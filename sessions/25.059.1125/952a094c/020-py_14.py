"""
The transformation rule involves identifying all non-white colored pixels within the input grid. Each of these pixels is mirrored across both the horizontal and vertical axes of the grid. The mirrored position is calculated by considering the center of the entire grid. If a pixel is already at its mirrored location, then it is simply duplicated at its existing position. The original pixels are not removed.
"""

import numpy as np

def get_grid_center(grid):
    # Calculate the center row and column indices of the grid.
    rows, cols = grid.shape
    row_center = (rows -1) / 2
    col_center = (cols -1) / 2
    return row_center, col_center

def mirror_position(pos, center):
    # Calculate the mirrored position of a pixel across the grid's center.
    row_center, col_center = center
    mirrored_row = int(2 * row_center - pos[0])
    mirrored_col = int(2 * col_center - pos[1])
    return (mirrored_row, mirrored_col)

def find_non_white_pixels(grid):
    # Find the positions and colors of all non-white pixels.
    non_white_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:  # Not white.
                non_white_pixels.append(((r, c), grid[r, c]))
    return non_white_pixels

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Get the center of the grid.
    center = get_grid_center(output_grid)

    # Find all non-white pixels.
    non_white_pixels = find_non_white_pixels(output_grid)

    # Mirror each non-white pixel across both axes.
    for (row, col), color in non_white_pixels:
        mirrored_pos = mirror_position((row, col), center)
        # Copy the color value to the mirrored position (original not cleared).
        output_grid[mirrored_pos] = color
        
    return output_grid