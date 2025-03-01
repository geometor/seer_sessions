"""
1.  **Identify Objects:** Find all contiguous regions of non-white pixels in the input grid. Record their color and pixel coordinates.
2.  **Determine output size:** The output size is 3x3
3.  **Identify intersecting shapes**:
    - If there are multiple objects and one is most-left and most-up, while the other is most-down and most-right, create an "L"-shape for the most-left/up using the first row/column, and an L-shape for the most-down/right using the last row/column.
    - If two objects intersect, create a 1-pixel wide "cross". The vertical element has the color of the object that extends vertically. The horizontal element has the color of the object that extends horizontally.
    - If just one object, it should have an L-shape. If the shape is most extended to bottom/right, create L using bottom row and last column, otherwise first row and column.

4.  **Populate Output Grid:** Fill the 3x3 output grid based on identified intersecting shapes.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append(
                    {"color": grid[row, col], "pixels": obj_pixels}
                )
    return objects

def get_extrema(obj):
    """get min row, max row, min col, max col"""
    rows = [p[0] for p in obj["pixels"]]
    cols = [p[1] for p in obj["pixels"]]
    return min(rows), max(rows), min(cols), max(cols)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)
    objects = find_objects(input_grid)

    # Handle single object case
    if len(objects) == 1:
        obj = objects[0]
        min_row, max_row, min_col, max_col = get_extrema(obj)
        if max_row > (input_grid.shape[0] / 2) or max_col > (input_grid.shape[1] /2):
          for i in range(3):
            output_grid[2,i] = obj["color"]
            output_grid[i,2] = obj["color"]
        else:
          for i in range(3):
            output_grid[0,i] = obj["color"]
            output_grid[i,0] = obj["color"]

    # handle multi-object cases
    elif len(objects) > 1:
      #Find top-left and bottom-right
      top_left_obj = None
      bottom_right_obj = None

      min_row_col_sum = float('inf')
      max_row_col_sum = float('-inf')
      for obj in objects:
        min_row, _, min_col, _ = get_extrema(obj)
        row_col_sum = min_row + min_col
        if row_col_sum < min_row_col_sum:
          min_row_col_sum = row_col_sum
          top_left_obj = obj
        
        _, max_row, _, max_col = get_extrema(obj)
        row_col_sum = max_row + max_col
        if row_col_sum > max_row_col_sum:
          max_row_col_sum = row_col_sum
          bottom_right_obj = obj
        

      #check for intersections
      intersect = False
      for p1 in top_left_obj["pixels"]:
        for p2 in bottom_right_obj["pixels"]:
          if p1 == p2:
            intersect = True
            break
        if intersect:
          break
      
      # handle intersect
      if intersect:
        # determine vertical and horizontal objects based on dimensions
        top_min_row, top_max_row, top_min_col, top_max_col = get_extrema(top_left_obj)
        bottom_min_row, bottom_max_row, bottom_min_col, bottom_max_col = get_extrema(bottom_right_obj)
          
        if (top_max_row - top_min_row) > (top_max_col - top_min_col):
            vertical_obj = top_left_obj
            horizontal_obj = bottom_right_obj
        else:
            vertical_obj = bottom_right_obj
            horizontal_obj = top_left_obj
        
        #Populate based on intersection
        for i in range(3):
          output_grid[i,1] = vertical_obj["color"]
          output_grid[1,i] = horizontal_obj["color"]
      
      #Handle L shapes
      else:
        for i in range(3):
          output_grid[0,i] = top_left_obj["color"]
          output_grid[i,0] = top_left_obj["color"]
        for i in range(3):
          output_grid[2,i] = bottom_right_obj["color"]
          output_grid[i,2] = bottom_right_obj["color"]
            
    return output_grid