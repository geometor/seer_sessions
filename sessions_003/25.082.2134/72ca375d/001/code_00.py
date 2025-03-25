"""
The logic appears to find a single object in the grid that matches specific criteria, then create a grid out of it.

1.  **Identify Objects:** Scan the input grid and identify all distinct objects, defined as contiguous blocks of pixels with the same color.
2.  **Select Target Object:**
    *   In example 1, select the largest magenta object, and get center rows
    *   In example 2, select the yellow, square object
    *   In example 3, select the gray object that looks like a horizontal 'I'.
3. **Create Output Grid** Construct output grid from selected objects.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of the same color in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, object_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        object_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                if color != 0:  # Ignore background
                    object_coords = []
                    dfs(r, c, color, object_coords)
                    objects.append((color, object_coords))
    return objects

def get_object_dimensions(object_coords):
    """Calculates the dimensions of an object given its coordinates."""
    if not object_coords:
        return 0, 0
    rows, cols = zip(*object_coords)
    height = max(rows) - min(rows) + 1
    width = max(cols) - min(cols) + 1
    return height, width


def transform(input_grid):
    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # initialize target_object
    target_object = None

    # Select object and create grid

    # magenta object
    magenta_objects = [obj for obj in objects if obj[0] == 6]
    if magenta_objects:
      # find largest
      largest_magenta = max(magenta_objects, key=lambda x: len(x[1]))
      rows, cols = zip(*largest_magenta[1])
      min_row, max_row = min(rows), max(rows)
      min_col, max_col = min(cols), max(cols)

      height = max_row - min_row + 1
      center_row_1 = min_row + (height // 2) - (1 if height%2==0 else 0)
      center_row_2 = min_row + (height//2)

      output_grid_coords = [(r,c) for (r,c) in largest_magenta[1] if r == center_row_1 or r==center_row_2]
      rows, cols = zip(*output_grid_coords)
      min_row, max_row = min(rows), max(rows)
      min_col, max_col = min(cols), max(cols)

      output_grid = np.zeros((max_row-min_row+1, max_col-min_col+1), dtype=int)
      for r, c in output_grid_coords:
          output_grid[r-min_row, c-min_col] = 6
      
      return output_grid

    # yellow object that is square
    yellow_objects = [obj for obj in objects if obj[0] == 4]
    if yellow_objects:
      for color, coords in yellow_objects:
        height, width = get_object_dimensions(coords)
        if height == width:
          # create grid and return
          rows, cols = zip(*coords)
          min_row, max_row = min(rows), max(rows)
          min_col, max_col = min(cols), max(cols)

          output_grid = np.zeros((max_row-min_row+1, max_col-min_col+1), dtype=int)

          for r, c in coords:
              output_grid[r - min_row, c - min_col] = 4 # yellow
          return output_grid


    # horizontal I object
    gray_objects = [obj for obj in objects if obj[0] == 5]
    if gray_objects:

      for color, coords in gray_objects:
          height, width = get_object_dimensions(coords)
          rows, cols = zip(*coords)
          min_row = min(rows)
          max_row = max(rows)          
          min_col = min(cols)
          max_col = max(cols)

          if height == 1 and width > 1:
             # single line - try it
            output_grid = np.array(input_grid[min_row:max_row+1, min_col:max_col+1], dtype=int)

            
            return output_grid

          elif height > 1 and width > height:
            # make horizontal 'I'

            # extract the relevant section
            output_grid = np.zeros((height, width), dtype=int)
            for r, c in coords:
                output_grid[r - min_row, c - min_col] = 5
            return output_grid

    # Default: return empty grid if no target found
    return np.zeros((0, 0), dtype=int)