"""
1.  **Preservation:** All red pixels in the input grid remain unchanged in the output grid.
2.  **Gray Removal:** All gray pixels in the input grid are replaced with white pixels in the output grid.
3.  **Conditional White Transformation:**
    *   White pixels that are *directly adjacent* (horizontally or vertically, but not diagonally) to a red pixel are transformed into blue pixels.
    * White pixels that are *directly adjacent* (horizontally or vertically, but not diagonally) to a *blue* pixel *and* are on the same row, or the row immediately below the red pixels, are converted to blue.
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonal=False):
    """
    Get the valid neighbors of a cell in a grid.
    """
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (dr == 0 and dc == 0) or (abs(dr) + abs(dc) > (1 if not include_diagonal else 2)):
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbors.append((new_row, new_col))
    return neighbors

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Gray Removal: replace all gray pixels (5) with white pixels (0)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                output_grid[r, c] = 0

    # Conditional White Transformation
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 0:  # Check white pixels in the output_grid
                neighbors = get_neighbors(output_grid, r, c)
                is_next_to_red = any(input_grid[nr, nc] == 2 for nr, nc in get_neighbors(input_grid, r, c)) #check input grid for original red
                if is_next_to_red:
                     output_grid[r,c] = 1
                else:
                    is_next_to_blue = any(output_grid[nr,nc] == 1 for nr, nc in neighbors)
                    # Find a red pixel to get the base row for blue extension
                    red_row = -1
                    for rr in range(rows):
                      for cc in range(cols):
                        if input_grid[rr,cc] == 2:
                           red_row = rr
                           break
                      if red_row != -1:
                         break
                    if is_next_to_blue and (r == red_row or r == red_row+1):
                        output_grid[r,c] = 1

    return output_grid