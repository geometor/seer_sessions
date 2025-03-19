"""
The transformation rule is as follows:

1.  **Initialization:** Create an output grid of the same dimensions as the input grid, initially filled with white pixels (value 0).

2.  **Magenta Preservation:** For every pixel in the input grid, if the pixel is magenta (value 6), set the corresponding pixel in the output grid to magenta.

3.  **Conditional Magenta Propagation:** For every pixel in the input grid:
    *   If the pixel is gray (value 5):
        *   Check if it is *diagonally adjacent* to any magenta pixel.
        *   Check if it is *directly adjacent* (up, down, left, or right) to any magenta pixel.
        *   If it is diagonally adjacent to a magenta pixel AND NOT directly adjacent to any magenta pixel, set the corresponding pixel in the output grid to magenta (value 6).

4.  **Default to White:** All other pixels in the input grid—those that are neither magenta, nor gray and satisfying the propagation condition—set to white (value 0) in the output grid.
"""

import numpy as np

def get_diagonally_adjacent_indices(row, col, height, width):
    """
    Returns a list of valid diagonally adjacent indices to a given cell.
    """
    adjacent_indices = []
    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < height and 0 <= new_col < width:
            adjacent_indices.append((new_row, new_col))
    return adjacent_indices

def get_adjacent_indices(row, col, height, width):
    """
    Returns a list of valid adjacent indices (up, down, left, right) to a given cell.
    """
    adjacent_indices = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < height and 0 <= new_col < width:
            adjacent_indices.append((new_row, new_col))
    return adjacent_indices

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # find magenta pixels
    magenta_pixels = []
    for r in range(height):
        for c in range(width):
            if input_grid[r,c] == 6:
                magenta_pixels.append((r,c))


    # change output pixels based on input
    for r in range(height):
        for c in range(width):
            if input_grid[r,c] == 6:
                # Magenta Preservation
                output_grid[r,c] = 6
            elif input_grid[r,c] == 5:
                # Conditional Magenta Propagation
                is_diagonally_adjacent = False
                for mr, mc in magenta_pixels:
                    if (r,c) in get_diagonally_adjacent_indices(mr, mc, height, width):
                       is_diagonally_adjacent = True
                       break

                is_adjacent = False
                for mr, mc in magenta_pixels:
                    if (r, c) in get_adjacent_indices(mr, mc, height, width):
                        is_adjacent = True
                        break

                if is_diagonally_adjacent and not is_adjacent:
                   output_grid[r,c] = 6
                else:
                    output_grid[r,c] = 0
            else:
                # Default to White
                output_grid[r,c] = 0

    return output_grid.tolist()