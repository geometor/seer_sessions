"""
The transformation rule involves moving non-zero pixels in the input grid to new positions in the output grid.
These new positions lie on diagonals, with the constraint that the sum of their row and column indices
equals the sum of the original row and column indices of the input pixel. The order is determined first by the
diagonal sum.  For pixels with the same diagonal sum, use the original row/column position in the input grid.
Within each diagonal, pixels are filled in sequentially.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving non-zero pixels to positions along diagonals,
    filling in based on diagonal sum and original position.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Non-zero Pixels and their diagonal sums.
    pixels = []
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != 0:
                pixels.append(((i, j), i + j, input_grid[i, j]))

    # 2. Sort pixels by diagonal sum, then by original row and column.
    pixels.sort(key=lambda x: (x[1], x[0][0], x[0][1]))

    # 3. Iterate through sorted pixels and place them in the output grid.
    for (orig_i, orig_j), diagonal_sum, color in pixels:
        
        placed = False
        for out_row in range(rows):
            out_col = diagonal_sum - out_row
            if 0 <= out_col < cols and output_grid[out_row,out_col] == 0:
                output_grid[out_row, out_col] = color
                placed = True
                break
        # should not occur, since ARC guarantees a solution
        if not placed:
            print("Error: could not place")

    return output_grid.tolist()