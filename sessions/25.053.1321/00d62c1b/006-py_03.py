"""
Iterates through each pixel in the input grid.
Identifies green (3) pixels.
For each green pixel, checks if it's the center of a "+" shaped structure formed by green pixels, with horizontal and vertical line segments of at least three contiguous green pixels.
If the condition is met, changes the pixel's color to yellow (4) in the output grid.
Pixels that are not green remain unchanged.
Returns the modified grid.
"""

import numpy as np

def get_line_length(grid, row, col, direction):
    """
    Calculates the length of a contiguous line of green pixels starting from a given position.

    Args:
        grid: The input grid.
        row: Starting row index.
        col: Starting column index.
        direction: A tuple (row_change, col_change) indicating the direction to check.
                   (0, 1) for horizontal (right), (0, -1) for horizontal (left),
                   (1, 0) for vertical (down), (-1, 0) for vertical (up).

    Returns:
        The length of the contiguous line of green pixels in the specified direction.
    """
    rows, cols = grid.shape
    length = 0
    r, c = row, col
    dr, dc = direction

    while 0 <= r < rows and 0 <= c < cols and grid[r, c] == 3:
        length += 1
        r += dr
        c += dc
    return length

def is_center_pixel(grid, row, col):
    """
    Checks if a green pixel is a "center" pixel, meaning it has green neighbors
    directly above, below, to the left, and to the right.

    Args:
        grid: The input grid.
        row: Row index of the pixel.
        col: Column index of the pixel.

    Returns:
        True if the pixel is a center pixel, False otherwise.
    """
    rows, cols = grid.shape
    if grid[row, col] != 3:
        return False

    # Check for neighbors in all four directions
    has_left   = col > 0 and grid[row, col - 1] == 3
    has_right  = col < cols - 1 and grid[row, col + 1] == 3
    has_above  = row > 0 and grid[row - 1, col] == 3
    has_below  = row < rows - 1 and grid[row + 1, col] == 3

    return has_left and has_right and has_above and has_below


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is green
            if output_grid[row, col] == 3:
                # Check for horizontal line segment of length >= 3
                left_length = get_line_length(output_grid, row, col - 1, (0, -1))
                right_length = get_line_length(output_grid, row, col + 1, (0, 1))
                horizontal_length = left_length + 1 + right_length  # Include the current pixel

                # Check for vertical line segment of length >= 3
                up_length = get_line_length(output_grid, row - 1, col, (-1, 0))
                down_length = get_line_length(output_grid, row + 1, col, (1, 0))
                vertical_length = up_length + 1 + down_length  # Include the current pixel

                # Check if it's a center pixel
                center_pixel = is_center_pixel(output_grid, row, col)

                # Change color to yellow if it's a center pixel and part of a line segment of length >= 3
                if center_pixel and horizontal_length >= 3 and vertical_length >= 3:
                    output_grid[row, col] = 4

    return output_grid