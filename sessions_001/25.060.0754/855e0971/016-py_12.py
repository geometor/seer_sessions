"""
The input is a grid divided in three horizontal colored sections. Within each colored section, there is a white pixel. We replicate the rows containing white pixels so that for each original row with a white pixel, there are *n* rows in the output, where *n* is the number of white pixels in the input.
"""

import numpy as np

def find_white_pixels(grid):
    # Find coordinates of all white pixels (value 0).
    white_pixels = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 0:
                white_pixels.append((i, j))
    return white_pixels

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    input_grid = np.array(input_grid)  # Ensure numpy array
    white_pixels = find_white_pixels(input_grid)
    num_white_pixels = len(white_pixels)
    rows_to_replicate = [coord[0] for coord in white_pixels]

    output_grid_rows = []

    for i in range(input_grid.shape[0]):
      output_grid_rows.append(input_grid[i])
      if i in rows_to_replicate:
        for _ in range(num_white_pixels -1):
          output_grid_rows.append(input_grid[i])

    output_grid = np.array(output_grid_rows)

    return output_grid