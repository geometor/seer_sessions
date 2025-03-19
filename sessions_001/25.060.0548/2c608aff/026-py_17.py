"""
The transformation identifies diagonally adjacent yellow (4) pixels in the input grid and connects them by changing the intervening blue (1) pixels to yellow (4) along a diagonal path. Pixels that are not blue (1) on this diagonal path are not changed.
"""

import numpy as np

def get_yellow_pixels(grid):
    # returns a list of coordinates of all yellow pixels
    yellow_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 4:
                yellow_pixels.append((row_index, col_index))
    return yellow_pixels

def get_diagonal_path(pixel1, pixel2):
    """
    Returns a list of coordinates representing the diagonal path between two pixels.
    Assumes pixel1 and pixel2 are diagonally aligned. Does not check for obstacles.
    """
    path = []
    row_diff = pixel2[0] - pixel1[0]
    col_diff = pixel2[1] - pixel1[1]
    row_step = 1 if row_diff > 0 else -1
    col_step = 1 if col_diff > 0 else -1

    row = pixel1[0] + row_step
    col = pixel1[1] + col_step

    while row != pixel2[0] and col != pixel2[1]:
        path.append((row, col))
        row += row_step
        col += col_step
    return path

def are_diagonally_adjacent(pixel1, pixel2, grid):
    """
    Checks if two pixels are diagonally adjacent and the path between them consists only of blue pixels.
    """
    row_diff = abs(pixel1[0] - pixel2[0])
    col_diff = abs(pixel1[1] - pixel2[1])

    if row_diff != col_diff or row_diff == 0:  # Not diagonal or same pixel
        return False

    path = get_diagonal_path(pixel1, pixel2)
    for r, c in path:
        if grid[r, c] != 1:
            return False # Path is not clear of non-blue pixels

    return True # if made through loop - all intervening pixels are blue



def transform(input_grid):
    """Transforms the input grid by connecting diagonally adjacent yellow pixels via blue pixels."""
    output_grid = np.copy(input_grid)
    yellow_pixels = get_yellow_pixels(input_grid)

    # Iterate through all pairs of yellow pixels
    for i in range(len(yellow_pixels)):
        for j in range(i + 1, len(yellow_pixels)):
            pixel1 = yellow_pixels[i]
            pixel2 = yellow_pixels[j]

            # Check for diagonal adjacency and clear path
            if are_diagonally_adjacent(pixel1, pixel2, input_grid):
                # Get the intervening pixels
                path = get_diagonal_path(pixel1, pixel2)

                # Change the intervening blue pixels to yellow
                for r, c in path:
                    output_grid[r, c] = 4

    return output_grid