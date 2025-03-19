"""
1. Identify Objects: Locate the single green pixel and the 2x2 magenta square within the input grid.
2. Expand Magenta Square: Expand the 2x2 magenta square by one pixel in all directions, creating a 4x4 magenta square.
3. Replicate and Position Green Pixels: Replicate the green pixel. Position a green pixel diagonally adjacent to each of the *four* corners of the *expanded* 4x4 magenta square. Specifically, place a green pixel one cell diagonally out from the top-left, top-right, bottom-left, and bottom-right corners of the expanded square.
"""

import numpy as np

def find_object(grid, color, shape=None):
    """Finds an object of a specific color and optionally shape."""
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return None

    if shape == "point":
      if len(coords) == 1:
        return coords[0]
      else:
        return None

    if shape == "2x2 square":
        min_row = np.min(coords[:, 0])
        max_row = np.max(coords[:, 0])
        min_col = np.min(coords[:, 1])
        max_col = np.max(coords[:, 1])

        if (max_row - min_row == 1) and (max_col - min_col == 1):
           return (min_row, min_col)  # Return top-left corner
        else:
          return None

    return coords

def expand_square(grid, top_left, old_size, new_size, color):
    """Expands a square object by one pixel in all directions."""
    row, col = top_left
    new_grid = np.copy(grid)
    # expand square by 1 on all sides
    start_row = row - 1
    start_col = col - 1
    for i in range(new_size):
        for j in range(new_size):
            if 0 <= start_row + i < grid.shape[0] and 0 <= start_col + j < grid.shape[1]:
              new_grid[start_row + i, start_col + j] = color

    return new_grid

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Identify Objects
    green_pixel_coord = find_object(input_grid, 3, "point")
    magenta_square_coord = find_object(input_grid, 6, "2x2 square")

    if green_pixel_coord is None or magenta_square_coord is None:
      return output_grid

    # 2. Expand Magenta Square
    output_grid = expand_square(output_grid, magenta_square_coord, 2, 4, 6)

    # get top left of expanded square
    expanded_top_left_row = magenta_square_coord[0] - 1
    expanded_top_left_col = magenta_square_coord[1] - 1

    # 3. Replicate and Position Green Pixels diagonally adjacent to corners.
    corners = [
        (expanded_top_left_row - 1, expanded_top_left_col - 1),  # Top-left
        (expanded_top_left_row - 1, expanded_top_left_col + 4),  # Top-right
        (expanded_top_left_row + 4, expanded_top_left_col - 1),  # Bottom-left
        (expanded_top_left_row + 4, expanded_top_left_col + 4),  # Bottom-right
    ]

    for row, col in corners:
        if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
            output_grid[row, col] = 3

    return output_grid