"""
The transformation rule is as follows:

1.  **Identify Blue Lines:** Locate all blue (1) pixels forming continuous vertical and horizontal lines. These lines act as barriers.
2.  **Flood Fill with Green:** Starting from any black(0) pixels, change to green(3) until a blue(1) pixel line is hit.
3. **Flood Fill with Yellow** Starting from any remaining black pixels, change to yellow(4) until a boundary consisting of any combination of 2 or more blue lines or the edge of the grid is hit.

"""

import numpy as np

def flood_fill(grid, start_row, start_col, fill_color, boundary_color):
    """
    Fills a region in the grid with the specified fill_color, starting from
    the given coordinates, until it encounters the boundary_color.
    """
    rows, cols = grid.shape
    if (start_row < 0 or start_row >= rows or
        start_col < 0 or start_col >= cols or
            grid[start_row, start_col] == fill_color or
            grid[start_row, start_col] == boundary_color):
        return

    grid[start_row, start_col] = fill_color

    flood_fill(grid, start_row + 1, start_col, fill_color, boundary_color)
    flood_fill(grid, start_row - 1, start_col, fill_color, boundary_color)
    flood_fill(grid, start_row, start_col + 1, fill_color, boundary_color)
    flood_fill(grid, start_row, start_col - 1, fill_color, boundary_color)

def transform(input_grid):
    """
    Transforms the input grid according to the rules described above.
    """
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # First, flood fill with green, treating blue as the boundary.
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                flood_fill(output_grid, r, c, 3, 1)

    # Create a temporary grid to correctly handle yellow fill.
    temp_grid = output_grid.copy()
    # Then, flood fill the remaining areas with yellow, considering blue as boundary, and the edge of the grid
    for r in range(rows):
        for c in range(cols):
          if temp_grid[r,c] == 0:
            output_grid[r,c] = 4


    return output_grid