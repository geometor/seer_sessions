"""
1.  **Identify two distinct objects.** An "inside object" which is a rectangle of non-zero pixels, and an "outside object" composed of one or more pixels located along the bottom edge of the input grid.
2.  **Locate the "outside object".**
3.  **Move the "outside object".** Reposition the outside object one row up and one column inward, making it adjacent to the "inside object".  If the outside object consists of multiple pixels, maintain their relative positions to each other during the move.
"""

import numpy as np

def find_objects(grid):
    # Find all contiguous blocks of non-zero pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                visited[r, c] = True
                color = grid[r,c]

                while stack:
                    curr_r, curr_c = stack.pop()
                    obj.append((curr_r, curr_c))
                    #check neighbors (up, down, left, right)
                    neighbors = [(curr_r - 1, curr_c), (curr_r + 1, curr_c),
                                 (curr_r, curr_c - 1), (curr_r, curr_c + 1)]
                    for nr, nc in neighbors:
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color and not visited[nr, nc]:
                            stack.append((nr, nc))
                            visited[nr, nc] = True
                objects.append(obj)
    return objects

def get_inside_outside_objects(objects, rows):
  outside_object = []
  inside_object = []
  for obj in objects:
    for r,c in obj:
      if r == rows-1:
        outside_object.extend(obj)
        break;
      else:
        inside_object.extend(obj)
        break;
  return inside_object, outside_object

def transform(input_grid):
    # Convert to numpy array
    grid = np.array(input_grid)
    rows, cols = grid.shape

    # 1. Identify two distinct objects
    objects = find_objects(grid)
    inside_object, outside_object = get_inside_outside_objects(objects, rows)
    
    # Initialize output grid as a copy
    output_grid = np.zeros_like(grid)

    #place the inside object
    for r, c in inside_object:
      output_grid[r,c] = grid[r,c]

    #2. Move the "outside object".
    if outside_object:
      #Find the bounding box of the inside object
      inside_rows = [r for r, _ in inside_object]
      inside_cols = [c for _, c in inside_object]
      min_inside_row = min(inside_rows)
      max_inside_row = max(inside_rows)
      min_inside_col = min(inside_cols)
      max_inside_col = max(inside_cols)
            
      # Calculate offsets relative to the bottom left
      for r,c in outside_object:
        output_grid[r-1, c-1 if c > 0 else 0] = grid[r,c]

    return output_grid.tolist()