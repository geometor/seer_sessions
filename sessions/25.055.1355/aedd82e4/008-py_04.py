"""
Preserve Reds: Copy the input grid to the output grid, leaving all pixels with the color red (2) unchanged.
Identify Blue Candidates: The pixels that were white in the input and in the bottom-right most location of contiguous white pixels in a row or column, adjacent to a red pixel, are candidates to become blue.
Change to Blue: The identified candidate pixels will change from color white(0) to color blue(1).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is white (0)
            if output_grid[r, c] == 0:
                # Check for adjacency to a red (2) pixel, and check if is the most bottom-right white pixel
                is_last_white_row = True
                is_last_white_col = True

                if r + 1 < rows:
                    if output_grid[r+1, c] == 0:
                        is_last_white_col = False

                if c + 1 < cols:
                  if output_grid[r,c+1] == 0:
                        is_last_white_row = False

                if is_last_white_col or is_last_white_row:

                    is_adjacent_to_red = False
                    # Check adjacent cells (up, down, left, right)
                    if r > 0 and output_grid[r - 1, c] == 2:
                        is_adjacent_to_red = True
                    if r < rows - 1 and output_grid[r + 1, c] == 2:
                        is_adjacent_to_red = True
                    if c > 0 and output_grid[r, c - 1] == 2:
                        is_adjacent_to_red = True
                    if c < cols - 1 and output_grid[r, c + 1] == 2:
                        is_adjacent_to_red = True

                    # Change the color to blue (1) if adjacent to red
                    if is_adjacent_to_red:
                      output_grid[r,c] = 1

    return output_grid