"""
The transformation rule involves identifying an initial shape made of magenta (color 6) pixels, 
expanding it, and creating new disconnected magenta shapes in the output grid while keeping 
the background white (color 0).
"""

import numpy as np

def get_shape(grid, color):
    """
    Extracts the coordinates of a connected shape of the specified color.
    """
    shape_coords = []
    visited = set()

    def dfs(row, col):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or grid[row, col] != color
            or (row, col) in visited
        ):
            return
        visited.add((row, col))
        shape_coords.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                dfs(r, c)
                return shape_coords  # Return the first shape found
    return shape_coords


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Get the initial magenta shape
    initial_shape_coords = get_shape(input_grid, 6)

    # Expand and fill the shape
    if initial_shape_coords:
        #expand horizontally, vertically, and diagonally
        for r, c in initial_shape_coords:
          for x in range(-1,2):
            for y in range (-1,2):
              output_grid[r+x,c+y] = 6

        min_row = min(r for r, c in initial_shape_coords)
        max_row = max(r for r, c in initial_shape_coords)
        min_col = min(c for r, c in initial_shape_coords)
        max_col = max(c for r, c in initial_shape_coords)

    # Create new shapes - mirror, below and to right of the initial shape
    if initial_shape_coords:
        center_row = (min_row + max_row) // 2
        center_col = (min_col + max_col) // 2

        # Mirror the shape
        for r, c in initial_shape_coords:
          #mirror across center
          mirrored_row = center_row + (center_row-r)
          mirrored_col = center_col + (center_col -c)

          if 0 <= mirrored_row < output_grid.shape[0] and 0 <= mirrored_col < output_grid.shape[1]:
            output_grid[mirrored_row,mirrored_col] = 6
            #expand the mirrored shape
            for x in range(-1,2):
              for y in range (-1,2):
                output_grid[mirrored_row+x,mirrored_col+y] = 6


    return output_grid