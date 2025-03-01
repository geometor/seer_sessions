"""
1.  **Identify Shapes:** Locate all contiguous regions of the same color in the input grid. These are our initial objects.

2.  **Background:** Determine the background, by looking for the color '0'

3.  **Color Changes:**
    *   Identify azure (8) colored shapes in the input.
    *   Maintain the 8 shape in the output.
    *   Change the color of the background adjacent to color 8.
       * Left: green (3)
       * Right: green(3)
       * Up: green (3)
       * Down: green(3)
        * Diagonal: green(3)
    * If inside an azure (8) object, change background to red(2).

4.  **Output:** Create the output grid by applying these color changes, keeping the shape and size of other colored regions in the same place.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                if obj:
                    objects.append((grid[row, col], obj))
    return objects
def is_inside(row, col, azure_object):
  """ Check if coordinate is within 8 object using a tolerance """
  min_r = min(r for r, c in azure_object)
  max_r = max(r for r, c in azure_object)
  min_c = min(c for r, c in azure_object)
  max_c = max(c for r, c in azure_object)
  
  return min_r <= row <= max_r and min_c <= col <= max_c

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find objects in input
    objects = find_objects(input_grid)

    # identify azure objects
    azure_objects = [obj for color, obj in objects if color == 8]
   
    # Iterate through each cell
    for r in range(rows):
        for c in range(cols):
            # skip non-background
            if output_grid[r,c] != 0:
                continue

            # default to background fill
            output_grid[r,c] = 3
            
            is_adj = False
            for ar, ac in [(r-1,c-1), (r-1,c), (r-1,c+1),
                           (r,  c-1), (r, c+1),
                           (r+1,c-1), (r+1, c), (r+1, c+1)]:
              if 0 <= ar < rows and 0 <= ac < cols:
                 if input_grid[ar, ac] == 8:
                    is_adj = True

            if is_adj:
              output_grid[r,c] = 3
            else:
                for color, azure_object in azure_objects: #check each object
                    if is_inside(r, c, azure_object):
                       output_grid[r,c] = 2
                       break

    return output_grid.tolist()