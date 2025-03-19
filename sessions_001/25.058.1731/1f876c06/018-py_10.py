"""
The transformation rule involves rotating the non-white pixels of the input grid 90 degrees clockwise, as if the entire grid was rotated, and placing them in a new grid with transposed dimensions. White pixels are treated as empty space in the input, and the background in the output.
"""

import numpy as np

def get_non_white_pixels(grid):
    """
    Returns a list of (color, (row, col)) tuples for non-white pixels,
    ordered from top-left to bottom-right.
    """
    non_white_pixels = []
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color != 0:
                non_white_pixels.append((color, (r, c)))
    return non_white_pixels

def calculate_new_position(old_row, old_col, input_height):
    """
    Calculates the new position of a pixel after a 90-degree clockwise rotation.
    """
    new_row = old_col
    new_col = input_height - 1 - old_row
    return new_row, new_col

def transform(input_grid):
    """
    Transforms the input grid by rotating its non-white pixels 90 degrees clockwise.
    """
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height, output_width = input_width, input_height

    # Identify Non-White Pixels
    non_white_pixels = get_non_white_pixels(input_grid)

    # Create Blank grid, fill all with white
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Calculate New Positions and Populate Output Grid
    for color, (old_row, old_col) in non_white_pixels:
        new_row, new_col = calculate_new_position(old_row, old_col, input_height)
        output_grid[new_row, new_col] = color

    return output_grid