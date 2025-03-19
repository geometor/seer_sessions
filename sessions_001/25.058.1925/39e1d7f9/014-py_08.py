"""
The transformation rule involves identifying rectangular shapes of magenta (6) pixels within a green (3) background. The magenta rectangles are then shifted one cell to the right. If a magenta pixel would move to a cell which already containes magenta, the move does *not* take place, it remains in its original cell.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and not visited[curr_r, curr_c]:
                        visited[curr_r, curr_c] = True
                        obj.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects.append(obj)
    return objects

def is_rectangle(obj, grid):
  """Checks if object is rectangle."""
  if not obj:
      return False

  rows, cols = zip(*obj)
  min_row, max_row = min(rows), max(rows)
  min_col, max_col = min(cols), max(cols)

  expected_size = (max_row - min_row + 1) * (max_col - min_col + 1)
  
  if len(obj) != expected_size:
    return False
  
  for r in range(min_row, max_row+1):
    for c in range(min_col, max_col+1):
      if (r,c) not in obj:
        return False

  return True

def shift_object_no_overlap(obj, output_grid, dc):
    # Shift the object horizontally by dc columns, wrapping around, but prevent overlap.
    rows, cols = output_grid.shape
    new_positions = []
    for r, c in obj:
        new_c = (c + dc) % cols
        new_positions.append((r, new_c))

    # Check for overlaps
    can_move = True
    for r, c in new_positions:
        if output_grid[r,c] != 3 and (r,c) not in obj :
            can_move = False
            break

    if can_move:
      #clear old positions:
      for r,c in obj:
        output_grid[r,c] = 3
      #move
      for r, c in new_positions:
          output_grid[r, c] = 6


def transform(input_grid):
    # Initialize output grid with the same values as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find magenta objects
    magenta_objects = find_objects(input_grid, 6)
    

    # Shift magenta objects one cell to the right.
    for obj in magenta_objects:
        if is_rectangle(obj, input_grid):
            shift_object_no_overlap(obj, output_grid, 1)

    return output_grid