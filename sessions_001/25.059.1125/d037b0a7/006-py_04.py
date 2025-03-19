"""
1.  **Identify Starting Points:** Locate all non-white pixels in the input grid. These are the "seed" pixels for the transformation.
2.  **Vertical Expansion (Yellow):** If a seed pixel is yellow (4), and there are adjacent white pixels *vertically*, change those adjacent white cells to yellow. This expansion is only one step.
3.  **Horizontal Expansion (Magenta):** If a seed pixel is magenta (6), change all adjacent white pixels to its *right* to magenta. Stop horizontal expansion when a non-white cell or the edge of the grid is encountered.
4. **Vertical and Horizontal Expansion(Magenta in top-left corner):** If magenta(6) appears at the top-left corner (0,0), it will propagate vertically down.
5. **Preserve other colors:** All other colors will be preserved.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the values of the immediate neighbors (up, down, left, right) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

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
                    neighbors = get_neighbors(input_grid, row, col)
                    for r, c in neighbors:
                        if input_grid[r,c] == 0 and abs(r-row) == 1 and abs(c-col)==0: # only vertically
                            output_grid[r, c] = 4
                # Horizontal Expansion (Magenta)
                elif input_grid[row, col] == 6:
                    # Special case: top-left corner
                    if row == 0 and col == 0:
                        for i in range(1, rows):
                             if input_grid[i,0] == 0:
                                 output_grid[i,0] = 6
                             else:
                                break

                    for c in range(col + 1, cols):
                        if input_grid[row, c] == 0:
                            output_grid[row, c] = 6
                        else:
                            break  # Stop at non-white or edge


    return output_grid