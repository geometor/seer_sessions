"""
The transformation rule is as follows:
1. Initialize an output grid of the same size as the input, filled with white (0).
2. Iterate through each pixel of the input grid.
3. If a pixel is magenta (6), set the corresponding output pixel to magenta.
4. If a pixel is gray (5) and diagonally adjacent to a magenta pixel, set the output pixel to magenta.
5. All other pixels, i.e., any gray pixels not diagonally adjacent to magenta, are converted to white.

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
                output_grid[r,c] = 6
            else:
                is_diagonally_adjacent = False
                for mr, mc in magenta_pixels:
                    if (r,c) in get_diagonally_adjacent_indices(mr, mc, height, width):
                       is_diagonally_adjacent = True
                       break

                if is_diagonally_adjacent:
                   output_grid[r,c] = 6
                # else it is 0, which is the default

    return output_grid.tolist()