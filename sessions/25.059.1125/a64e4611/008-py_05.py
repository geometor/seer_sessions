"""
The transformation rule identifies a rectangular region of white (0) pixels within the input grid and replaces them with green (3) pixels in the output grid. Blue (1) pixels remain unchanged. The rectangle has a specific shape.
"""

import numpy as np

def get_objects(grid, color):
    """
    Find contiguous regions (objects) of a specific color in the grid.
    
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return []

        visited[row, col] = True
        object_pixels = [(row, col)]

        object_pixels.extend(dfs(row + 1, col))
        object_pixels.extend(dfs(row - 1, col))
        object_pixels.extend(dfs(row, col + 1))
        object_pixels.extend(dfs(row, col - 1))
        return object_pixels

    for row in range(rows):
      for col in range(cols):
          if grid[row, col] == color and not visited[row, col]:
            objects.append(dfs(row, col))

    return objects
    

def find_enclosed_rows_and_cols(grid, objects, color):
    rows, cols = grid.shape
    enclosed_rows = set()
    enclosed_cols = set()

    for obj in objects:
        min_row = min(pixel[0] for pixel in obj)
        max_row = max(pixel[0] for pixel in obj)
        min_col = min(pixel[1] for pixel in obj)
        max_col = max(pixel[1] for pixel in obj)

        if min_row == 0 or max_row == rows-1:
          for r in range(min_row,max_row+1):
            enclosed_rows.add(r)
        if min_col == 0 or max_col == cols - 1:
          for c in range(min_col,max_col+1):
            enclosed_cols.add(c)
          
    return enclosed_rows, enclosed_cols


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # get the blue objects
    blue_objects = get_objects(input_grid, 1)

    # find the rows and cols to fill
    fill_rows, fill_cols = find_enclosed_rows_and_cols(input_grid,blue_objects, 1)

    # fill those rows and cols with green, except where the blue is
    for r in range(rows):
      for c in range(cols):
        if (r in fill_rows or c in fill_cols) and input_grid[r,c] == 0:
          output_grid[r,c] = 3

    return output_grid