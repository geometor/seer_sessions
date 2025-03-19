"""
Transforms an input grid to an output grid by inverting the colors of a
"cross" shaped object and its background, while keeping the border unchanged.
Color inversions follow these pairs: gray <-> yellow, red <-> blue.
"""

import numpy as np

def get_cross_coords(grid):
    rows, cols = grid.shape
    center_row, center_col = rows // 2, cols // 2
    cross_coords = []

    # Vertical parts of the cross
    for r in range(1, rows - 1):
      if (r >= center_row - 1 and r <= center_row + 1):
          continue # the center 2x2 block
      cross_coords.append((r, center_col -1))
      cross_coords.append((r, center_col))

    # Horizontal parts of the cross
    for c in range(1, cols - 1):
      if (c >= center_col - 1 and c <= center_col):
          continue # the center 2x2 block
      cross_coords.append((center_row - 1, c))
      cross_coords.append((center_row, c))
    return cross_coords

def invert_color(color):
    if color == 8:
        return 4
    elif color == 4:
        return 8
    elif color == 2:
        return 1
    elif color == 1:
        return 2
    else:
        return color

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # Get coordinates of the "cross"
    cross_coords = get_cross_coords(input_grid)

    # Invert colors on the cross and background, leave border unchanged
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if (r, c) in cross_coords or \
               (r < rows -1 and c < cols -1 and
                input_grid[r, c] != input_grid[0,0] and
                input_grid[r,c] != input_grid[0, cols -1] and
                input_grid[r,c] != input_grid[rows-1, 0] and
                input_grid[r,c] != input_grid[rows -1, cols -1]):
                output_grid[r, c] = invert_color(input_grid[r, c])

    return output_grid