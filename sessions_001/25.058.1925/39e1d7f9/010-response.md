# 39e1d7f9 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves identifying rectangular shapes of magenta (6) and yellow (4) pixels within a green (3) background. The magenta rectangles, except the ones including yellow rectangles, are then shifted one cell to the right.
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

def shift_object(obj, output_grid, dc):
    # Shift the object horizontally by dc columns.
    for r, c in obj:
        output_grid[r, c + dc] = output_grid[r,c]
        output_grid[r,c] = 3 #background color


def transform(input_grid):
    # Initialize output grid with the same values as the input grid.
    output_grid = np.copy(input_grid)

    # Find magenta and yellow objects
    magenta_objects = find_objects(input_grid, 6)
    yellow_objects = find_objects(input_grid, 4)
    
    #Create combined objects
    combined_objects = []
    
    for m_obj in magenta_objects:
      if is_rectangle(m_obj, input_grid):
        for y_obj in yellow_objects:
            y_rows, y_cols = zip(*y_obj)
            min_y_row, max_y_row = min(y_rows), max(y_rows)
            min_y_col, max_y_col = min(y_cols), max(y_cols)

            m_rows, m_cols = zip(*m_obj)
            min_m_row, max_m_row = min(m_rows), max(m_rows)
            min_m_col, max_m_col = min(m_cols), max(m_cols)          
            if min_m_row <= min_y_row and max_m_row >= max_y_row and min_m_col <= min_y_col and max_m_col >= max_y_col:
              combined_objects.append(m_obj)

    # Shift magenta objects one cell to the right, if they are not combined
    for obj in magenta_objects:
        if is_rectangle(obj, input_grid) and obj not in combined_objects:
              shift_object(obj, output_grid, 1)

    return output_grid
```
