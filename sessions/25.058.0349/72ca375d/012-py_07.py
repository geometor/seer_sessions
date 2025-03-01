"""
1.  Identify all 2x2 yellow squares in the input grid.
2.  If a 2x2 yellow square is found, select it as the output.
3.  If no 2x2 yellow square is present, but there is a single, unique 2x2 square of any color, select the unique 2x2 square.
4.  The extracted square object becomes the output grid. All other regions are discarded.
"""

import numpy as np

def find_objects(grid):
    objects = []
    visited = set()

    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]):
            return []

        visited.add((row, col))
        object_pixels = [(row, col)]
        color = grid[row, col]

        object_pixels.extend(dfs(row + 1, col))
        object_pixels.extend(dfs(row - 1, col))
        object_pixels.extend(dfs(row, col + 1))
        object_pixels.extend(dfs(row, col - 1))

        # Check if all pixels have same color.
        if all(grid[r][c] == color for r, c in object_pixels):
          return object_pixels
        else:
          return []

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            result = dfs(row, col)
            if len(result)>0:
              objects.append(result)

    return objects


def get_object_bounds(object_pixels):
    min_row = min(p[0] for p in object_pixels)
    max_row = max(p[0] for p in object_pixels)
    min_col = min(p[1] for p in object_pixels)
    max_col = max(p[1] for p in object_pixels)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find all yellow objects
    yellow_objects = find_objects(input_grid)

    # Find all 2x2 yellow squares
    target_objects = []
    for obj in yellow_objects:
        min_row, max_row, min_col, max_col = get_object_bounds(obj)
        if (max_row - min_row + 1) == 2 and (max_col - min_col + 1) == 2 and input_grid[min_row, min_col] == 4:
            target_objects.append(obj)

    # Extract the first 2x2 yellow square, if any.
    if target_objects:
        min_row, max_row, min_col, max_col = get_object_bounds(target_objects[0])
        output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
        return output_grid

    # find all 2x2 squares
    squares = []
    all_objects = find_objects(input_grid)
    for obj in all_objects:
      min_row, max_row, min_col, max_col = get_object_bounds(obj)
      if (max_row - min_row + 1) == 2 and (max_col - min_col + 1) == 2:
          squares.append(obj)

    # If no 2x2 yellow square, return unique 2x2 square
    if len(squares) == 1:
      min_row, max_row, min_col, max_col = get_object_bounds(squares[0])
      output_grid = input_grid[min_row:max_row + 1, min_col:max_col + 1]
      return output_grid
      
    return None