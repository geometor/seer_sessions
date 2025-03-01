"""
1.  **Identify Starting Points:** Locate all non-white pixels in the input grid. These are the "seed" pixels for the transformation.
2.  **Vertical Expansion (Yellow):** If a seed pixel is yellow (4), extend a line of yellow pixels upwards and downwards as far as possible, until another color or the edge of the grid is encountered.
3.  **Horizontal Expansion (Magenta):** If a seed pixel is magenta (6), extend a line of magenta to the right until another color or the edge of the grid is encountered.
4. **Vertical and Horizontal Expansion(Magenta in top-left corner):** If magenta(6) appears at the top-left corner (0,0), it extends vertically down, irrespective of other colors. It also behaves as a normal magenta expanding to the right.
5. **Preserve other colors:** All other colors will be preserved.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel to find seed pixels
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] != 0:
                # Vertical Expansion (Yellow)
                if input_grid[row, col] == 4:
                    # Extend upwards
                    for r in range(row - 1, -1, -1):
                        if output_grid[r, col] == 0:
                            output_grid[r, col] = 4
                        else:
                            break
                    # Extend downwards
                    for r in range(row + 1, rows):
                        if output_grid[r, col] == 0:
                            output_grid[r, col] = 4
                        else:
                            break

                # Horizontal Expansion (Magenta)
                elif input_grid[row, col] == 6:
                    # Special case: top-left corner
                    if row == 0 and col == 0:
                        for i in range(0, rows):
                             output_grid[i,0] = 6

                    # Extend to the right
                    for c in range(col + 1, cols):
                        if output_grid[row, c] == 0:
                            output_grid[row, c] = 6
                        else:
                            break  # Stop at non-white or edge

    return output_grid