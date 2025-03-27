"""
1.  **Identify the Center:** Find the coordinates (row, column) of the single '0' pixel within the input grid.
2.  **Determine Cross Color:** Identify the color of the non-zero pixels adjacent to the zero pixel in the input grid.
3.  **Create Output Grid:** Initialize an output grid of the same dimensions as the input grid, filled entirely with '0'.
4.  **Draw Cross:**
      - Draw the color of the cross on the output grid
      - The center of the cross must be at the coordinates of the '0' from the input grid.
      - Extend lines from the center, along the row and column, until the edge of the output grid is met.
"""

import numpy as np

def find_center(grid):
    # Find the coordinates of the '0' pixel.
    rows, cols = np.where(grid == 0)
    return rows[0], cols[0]

def get_surrounding_color(grid):
    # get color of pixels surrounding the '0'
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] != 0:
                return grid[r,c]
    return 0 # default to 0 if no other color is found


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Find the center (coordinates of the '0' pixel).
    center_row, center_col = find_center(input_grid)
    surrounding_color = get_surrounding_color(input_grid)


    # Draw Cross
    for r in range(rows):
        output_grid[r, center_col] = surrounding_color  # Vertical line
    for c in range(cols):
        output_grid[center_row, c] = surrounding_color  # Horizontal line

    output_grid[center_row,center_col] = 0


    return output_grid.tolist()