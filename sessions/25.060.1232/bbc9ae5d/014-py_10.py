"""
The initial transformation rule identifies the largest square of non-zero pixels in the input grid. The output grid is a copy of the input grid, but with all pixels outside of this largest square set to zero (white). If no non-zero pixels are found, the output is an all-zero grid.
"""

import numpy as np

def find_largest_square(grid):
    # Find the largest square of non-zero pixels.
    rows, cols = grid.shape
    max_size = 0
    top_left = (0, 0)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                for size in range(1, min(rows - r, cols - c) + 1):
                    valid_square = True
                    for i in range(r, r + size):
                        for j in range(c, c + size):
                            if grid[i, j] == 0:
                                valid_square = False
                                break
                        if not valid_square:
                            break
                    if valid_square:
                        if size > max_size:
                            max_size = size
                            top_left = (r, c)

    return top_left, max_size

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the largest square of non-zero pixels.
    top_left, size = find_largest_square(input_grid)

    # Set all pixels outside the largest square to zero.
    for r in range(rows):
        for c in range(cols):
            if not (top_left[0] <= r < top_left[0] + size and
                    top_left[1] <= c < top_left[1] + size):
                output_grid[r, c] = 0

    return output_grid