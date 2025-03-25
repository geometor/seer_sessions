"""
1.  **Identify Source Pixels:** Find all non-zero pixels in the input grid. These are the "source" pixels.
2.  **Downward Propagation:** For each source pixel:
    *   Propagate its color downwards in the same column, replacing any zeros. Stop when a non-zero pixel or the bottom edge of the grid is encountered.
3.  **Diagonal Propagation:** For each source pixel:
    *   Propagate its color diagonally down and to the right (increasing row and column index), replacing any zeros.
    *   Stop when:
        *   A non-zero pixel is encountered.
        *   The edge of the grid is reached.
        *   The cell directly below the current cell in the downward propagation, relative to the *source* pixel's column, is non-zero. This means if a color has *not* propagated vertically to the row below the position of the diagonal propagation, the diagonal stops.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all pixels to identify source pixels (non-zero)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                color = input_grid[r, c]

                # Downward Propagation
                for row_below in range(r + 1, rows):
                    if output_grid[row_below, c] == 0:
                        output_grid[row_below, c] = color
                    else:
                        break  # Stop at non-zero or edge

                # Diagonal Propagation
                row_diag, col_diag = r + 1, c + 1
                while row_diag < rows and col_diag < cols:
                    # Check the new stopping condition:
                    if output_grid[row_diag, c] != 0 :
                        break

                    if output_grid[row_diag, col_diag] == 0:
                        output_grid[row_diag, col_diag] = color

                    else:
                        break  # Stop at non-zero or edge
                    row_diag += 1
                    col_diag += 1

    return output_grid