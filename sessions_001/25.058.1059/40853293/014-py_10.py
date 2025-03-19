"""
1.  **Identify Yellow Pixels:** Locate all pixels with the color yellow (value 4) in the input grid.
2.  **Vertical Expansion (Yellow):** For each yellow pixel, extend its color downwards. The expansion continues until the edge of the grid is reached or a pixel that has a value is encountered (not including background).
3.  **Identify Expansion Rows:** Determine the rows that contain vertically expanded yellow pixels.
4.  **Horizontal Expansion (Other Colors):** Within each row identified in step 3, expand any non-yellow and non-background color horizontally.  This expansion occurs in both directions (left and right). The expansion of a color stops when it encounters a pixel of a *different* color, or the edge of the grid. The color being expanded determines fill color, not the yellow.
"""

import numpy as np

def get_yellow_pixels(grid):
    """Finds the coordinates of all yellow (4) pixels."""
    yellow_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 4:
                yellow_pixels.append((r, c))
    return yellow_pixels

def expand_vertically(grid, start_row, col):
    """Expands yellow (4) pixels downwards until another object or edge."""
    rows = grid.shape[0]
    current_row = start_row

    while current_row < rows:
        if grid[current_row,col] != 0 and grid[current_row,col] !=4:
            break
        grid[current_row, col] = 4
        current_row += 1

def expand_horizontally_refined(grid):
    """Expands colored pixels horizontally, respecting boundaries."""
    rows = grid.shape[0]
    cols = grid.shape[1]

    for r in range(rows):
      if 4 in grid[r]:
        # expand left to right
        for c in range(cols):
            if grid[r, c] != 4 and grid[r, c] != 0:
                original_color = grid[r, c]
                # expand right
                for dc in range(c+1,cols):
                  if grid[r,dc] == 4:
                    grid[r, dc] = original_color
                  else:
                    break
                # expand left
                for dc in range(c-1,-1,-1):
                  if grid[r,dc] == 4:
                    grid[r,dc] = original_color
                  else:
                    break

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find yellow pixel coordinates
    yellow_pixels = get_yellow_pixels(output_grid)

    # expand the yellow pixels vertically
    for r, c in yellow_pixels:
        expand_vertically(output_grid, r, c)

    # expand other colored pixels horizontally, respecting boundaries
    expand_horizontally_refined(output_grid)

    return output_grid