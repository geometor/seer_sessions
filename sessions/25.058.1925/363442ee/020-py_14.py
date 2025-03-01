"""
1.  **Check for Identity:** If the input grid consists of a single, uniform color, or has repeating alternating vertical bars of color, or if a repeating pattern of alternating colored columns exists throughout, the output is identical to the input.
2.  **Check for Color Replacement:** If the input grid contains a single vertical line of a uniform color, and the rest of the grid is a uniform color, replace the line's color with the grid's main color.
3.  **Check for Cyclic Shift:** If the input grid's rows (or possibly columns) consist of a sequence of colors, and each subsequent row (or column) is a cyclic shift of the previous one, perform a cyclic shift of each row one position to the *right*.
"""

import numpy as np

def is_uniform(grid):
    """Checks if the grid is of a single, uniform color."""
    return np.all(grid == grid[0, 0])

def has_alternating_vertical_bars(grid):
    """Checks if the grid has repeating alternating vertical bars of color."""
    _, width = grid.shape
    if width < 2:  # Need at least two columns to alternate
        return False

    for x in range(2, width):
        if not np.array_equal(grid[:, x], grid[:, x % 2]):
            return False
    return True

def has_alternating_columns(grid):
    """Checks for a repeating pattern of alternating colored columns."""
    height, width = grid.shape
    if width < 2:
        return False

    for x in range(2, width):
        for y in range(height):
            if grid[y,x] != grid[y, x%2]:
                return False
    return True


def find_single_vertical_line(grid):
    """Finds a single vertical line of uniform color. Returns x, color or -1, -1"""
    height, width = grid.shape
    for x in range(width):
        color = grid[0, x]
        is_line = True
        for y in range(1, height):
            if grid[y, x] != color:
                is_line = False
                break
        if is_line:
            return x, color
    return -1, -1

def is_rest_of_grid_uniform(grid, exclude_x):
    """Checks if the rest of the grid, excluding a column, is uniform."""
    height, width = grid.shape
    first_color = -1

    for y in range(height):
        for x in range(width):
            if x != exclude_x:
                if first_color == -1:
                    first_color = grid[y, x]
                elif grid[y, x] != first_color:
                    return False
    return True

def cyclic_shift_right(arr):
    """Cyclically shifts a 1D array one position to the right."""
    return np.roll(arr, 1)

def is_cyclic_shift_rows(grid):
    """Checks if each row is a cyclic shift of the previous one."""
    height, width = grid.shape
    for i in range(1, height):
        if not np.array_equal(cyclic_shift_right(grid[i-1]), grid[i]):
            return False
    return True

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    height, width = input_grid.shape

    # 1. Check for Identity
    if is_uniform(input_grid) or has_alternating_vertical_bars(input_grid) or has_alternating_columns(input_grid):
        return output_grid

    # 2. Check for Color Replacement
    line_x, line_color = find_single_vertical_line(input_grid)
    if line_x != -1 and is_rest_of_grid_uniform(input_grid, line_x):
        main_color = input_grid[0, 0] if line_x != 0 else input_grid[0,1]
        for y in range(height):
            output_grid[y, line_x] = main_color
        return output_grid

    # 3. Check for Cyclic Shift
    if is_cyclic_shift_rows(input_grid):
        for i in range(height):
            output_grid[i] = cyclic_shift_right(input_grid[i])
        return output_grid

    return output_grid