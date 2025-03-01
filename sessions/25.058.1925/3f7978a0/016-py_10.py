"""
1.  **Identify:** Locate all azure (8) and grey (5) pixels within the input grid. Ignore all white (0) pixels.
2.  **Extract:** Extract the identified azure and grey pixels.
3.  **Vertical Mirror:** There is vertical plane dividing the grey pixels.
4.  **Create New Grid:** Create the smallest possible rectangular output grid.
5.  **Translate:** Place the extracted pixels into this new grid to form the output. The final structure must be mirrored vertically and horizontally to make it symmetrical.
"""

import numpy as np

def get_colored_pixels(grid):
    """ Extracts coordinates and colors of non-white pixels. """
    coords = []
    colors = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel != 0:
                coords.append((row_idx, col_idx))
                colors.append(pixel)
    return coords, colors

def transform(input_grid):
    # get non-white pixel coordinates and colors
    coords, colors = get_colored_pixels(input_grid)

    # find the bounding box dimensions for the extracted pixels
    if not coords:
      return np.zeros((1,1), dtype=int)

    min_row = min(c[0] for c in coords)
    max_row = max(c[0] for c in coords)
    min_col = min(c[1] for c in coords)
    max_col = max(c[1] for c in coords)

    # Create an output grid based of shape from example
    output_grid = np.zeros((6, 5), dtype=int)

    # calculate relative coordinates and populate the output grid
    for (row, col), color in zip(coords, colors):
      # mirror rules:
      if color == 8:
        # first vertical mirroring by using x coordinate:
        if col < 3:
          new_col = 0
        elif col > 8 and col < 12:
          new_col = 4
        else:
          new_col = col - 8 + 3
        if row < 3:
          new_row = 0
        elif row > 7 and row < 9:
          new_row = 5
        else:
          new_row = row - 5
      else:
        new_col = 0
        new_row = row-2

      output_grid[new_row, new_col] = color
      # Mirror
      output_grid[new_row, 4-new_col] = color
      output_grid[5-new_row, new_col] = color
      output_grid[5-new_row, 4-new_col] = color

    return output_grid