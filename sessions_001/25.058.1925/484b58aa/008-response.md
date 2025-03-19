# 484b58aa • 008 • refine_coder

---
```python
"""
1.  Examine the input grid: Identify all contiguous objects, noting their color, shape, and position.
2.  Color Change (Conditional): If there is an object of color 1, change its color to 2 in the output grid.  Preserve its shape and position.
3. Object Extraction (Conditional): If there is only a *single* object with color 3 surrounded *entirely* by black, extract the object with color 3 into output. Remove all black pixels. The output will have the dimensions to include the extracted object only.
4.  Object Preservation: If an object of color 8 exists, preserve its original shape, color and position in the output.
5.  Default: If no specific transformation rule applies, the output should be an empty grid. (This is implied by the need to return something, and the possibility of no objects matching the above criteria).
"""

import numpy as np

def get_objects(grid):
    """Identifies contiguous objects of the same color."""
    objects = []
    visited = set()

    def dfs(row, col, color, obj_coords):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return

        visited.add((row, col))
        obj_coords.append((row, col))
        # Explore adjacent cells
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if obj_coords:
                    objects.append(
                        {
                            "color": color,
                            "coordinates": obj_coords,
                            "shape": "contiguous",
                        } # Simplified for now
                    )
    return objects

def extract_object(grid, object_coords):
    """Extracts an object from the grid given its coordinates."""
    rows = [c[0] for c in object_coords]
    cols = [c[1] for c in object_coords]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    output_grid = np.zeros((output_height, output_width), dtype=int)
    for row, col in object_coords:
        output_grid[row - min_row, col - min_col] = grid[row, col]
    return output_grid


def transform(input_grid):
    # initialize output_grid to be the same as input (for preservation)
    output_grid = np.copy(input_grid)

    # get all objects
    input_objects = get_objects(input_grid)

    # Color change 1 -> 2
    for obj in input_objects:
        if obj["color"] == 1:
            for row, col in obj["coordinates"]:
                output_grid[row, col] = 2

    #Object extraction, only applies if there's only one object of color 3
    color3_objects = [obj for obj in input_objects if obj["color"] == 3]
    if len(color3_objects) == 1:
      #check if the color 3 object is surrounded by 0
      coords = color3_objects[0]["coordinates"]
      rows = [c[0] for c in coords]
      cols = [c[1] for c in coords]
      min_row, max_row = min(rows), max(rows)
      min_col, max_col = min(cols), max(cols)

      is_surrounded = True
      # check top
      if min_row > 0:
          for c in range(min_col,max_col+1):
              if input_grid[min_row-1,c]!=0:
                  is_surrounded = False
                  break
      #check bottom
      if is_surrounded and max_row < input_grid.shape[0]-1:
           for c in range(min_col,max_col+1):
              if input_grid[max_row+1,c]!=0:
                  is_surrounded = False
                  break
      #check left
      if is_surrounded and min_col > 0:
          for r in range(min_row,max_row+1):
              if input_grid[r,min_col-1]!=0:
                  is_surrounded=False
                  break
      #check right
      if is_surrounded and max_col < input_grid.shape[1]-1:
           for r in range(min_row,max_row+1):
              if input_grid[r,max_col+1]!=0:
                  is_surrounded=False
                  break

      if is_surrounded:
          output_grid = extract_object(input_grid, color3_objects[0]["coordinates"])

    # if no conditions met, return empty grid
    if len(input_objects) == 0:
        return np.array([])
    return output_grid
```
