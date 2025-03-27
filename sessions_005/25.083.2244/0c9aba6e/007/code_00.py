"""
Finds a horizontal line of orange (7) pixels in the input grid.
Identifies "L" shapes (groups of three connected magenta pixels forming a right angle) in the section of the input grid below the orange line.
Replaces these "L" shapes with azure (8) pixels in the output grid, maintaining their original relative positions.
Returns only the section of the grid below the separator.
"""

import numpy as np

def find_separator_row(grid):
    """Finds the row index of the separator line (all 7s)."""
    for i, row in enumerate(grid):
        if all(pixel == 7 for pixel in row):
            return i
    return -1  # Separator not found

def is_valid_l_shape(pixels, grid):
    """Checks if a set of three pixels forms a valid L shape."""
    if len(pixels) != 3:
        return False

    # Sort pixels by row and then by column
    pixels.sort()

    # Check for the two possible L-shape configurations
    if (pixels[0][0] == pixels[1][0] and  # Two pixels in the same row
        pixels[1][1] == pixels[2][1] and  # Two pixels in the same column
        pixels[1][0] == pixels[2][0] - 1 and  # Vertical offset of 1
        pixels[0][1] == pixels[1][1] - 1):    # horizontal offset of 1
        return True
    elif (pixels[0][1] == pixels[1][1] and
        pixels[1][0] == pixels[2][0] and
        pixels[0][0] == pixels[1][0] -1 and
        pixels[1][1] == pixels[2][1] - 1):
        return True
    else:
        return False

def find_l_shapes_below_separator(grid, separator_row):
    """Finds "L" shapes in the section of the grid below the separator."""
    l_shapes = []
    rows, cols = grid.shape
    visited = set()

    def explore(r, c, current_l_shape):
        if (
            r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or grid[r, c] != 6
        ):
            return

        visited.add((r, c))
        current_l_shape.append((r, c))

        # Explore adjacent neighbors
        explore(r + 1, c, current_l_shape)
        explore(r - 1, c, current_l_shape)
        explore(r, c + 1, current_l_shape)
        explore(r, c - 1, current_l_shape)
    for r in range(separator_row + 1, rows):  # Iterate only below the separator
        for c in range(cols):
             if grid[r, c] == 6 and (r, c) not in visited:
                current_l_shape = []
                explore(r, c, current_l_shape)
                if is_valid_l_shape(current_l_shape, grid):
                    l_shapes.append(current_l_shape)
    return l_shapes

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Find the separator row
    separator_row_index = find_separator_row(input_grid)

    # Handle cases where separator is not found
    if separator_row_index == -1:
        return input_grid.tolist()

    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find L-shapes below the separator
    l_shapes = find_l_shapes_below_separator(input_grid, separator_row_index)

    # Transform identified L-shapes to azure (8) in entire grid
    for l_shape in l_shapes:
        for r, c in l_shape:
            output_grid[r, c] = 8

    # Return the section of the grid below the separator
    return output_grid[separator_row_index + 1:].tolist()