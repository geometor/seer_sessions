```python
"""
The transformation extracts a sub-grid from the input grid. The output grid's colors are a subset of the input grid's colors. The size and location of the subgrid appears related to largest object(s) in the input and/or colors 1 and 2 if they exist,
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects (regions of same color) in a grid.
    Returns a dictionary where keys are colors and values are lists of object coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r][c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def get_object_bounding_box(obj_coords):
    """
    Returns the bounding box (min_row, min_col, max_row, max_col) for an object.
    """
    if not obj_coords:
        return None
    min_row = min(coord[0] for coord in obj_coords)
    min_col = min(coord[1] for coord in obj_coords)
    max_row = max(coord[0] for coord in obj_coords)
    max_col = max(coord[1] for coord in obj_coords)
    return min_row, min_col, max_row, max_col

def get_largest_object(objects):
    """Find and return the largest object's color and coordinates."""
    largest_obj_color = -1
    largest_obj_size = 0
    largest_obj_coords = []

    for color, obj_list in objects.items():
      for obj_coords in obj_list:
        size = len(obj_coords)
        if size > largest_obj_size:
          largest_obj_size = size
          largest_obj_color = color
          largest_obj_coords = obj_coords
    return largest_obj_color, largest_obj_coords

def transform(input_grid):
    input_grid_np = np.array(input_grid)
    objects = find_objects(input_grid_np)
    largest_obj_color, largest_obj_coords = get_largest_object(objects)

    # Case 1: Color 1 exists
    if 1 in objects:
        #Find bounding box
        bbox = get_object_bounding_box(objects[1][0]) # Assumes object of color 1 is not disjointed

        output_grid = []

        # Attempt to extract a 2x2 sub-grid
        for i in range(2):
            row = []
            for j in range(2):
              try:
                row.append(input_grid_np[bbox[0] + i][bbox[1] + j])

              except:
                return [[-1]] #Invalid output

            output_grid.append(row)

        # Check if 2 exists in the extracted grid
        output_grid_np = np.array(output_grid)
        if 2 not in output_grid_np and len(objects[1]) > 1: # if 2 does not exist and the size of objects of color 1

            for obj_list in objects.values():
                for obj_coords in obj_list:

                    bbox_obj = get_object_bounding_box(obj_coords)

                    for r in range(bbox_obj[0], bbox_obj[2] + 1):
                        for c in range(bbox_obj[1], bbox_obj[3]+ 1):
                            if input_grid[r][c] == 2:
                                output_grid = []
                                try:
                                    for i in range(2):
                                        row = []
                                        for j in range(2):
                                            row.append(input_grid_np[r+i][c+j])
                                        output_grid.append(row)
                                    output_grid_np = np.array(output_grid) #Update output
                                    if 1 in output_grid_np:
                                        return output_grid.tolist() # Return if we find 1 and 2 in proximity

                                except IndexError:
                                    pass # Keep trying
        return output_grid


    # Case 2: If only one dominant color
    elif len(objects) == 1 or (len(objects) == 2 and 0 in objects and len(objects[0]) == 1 ):

        return [[input_grid_np[0][0]]] # return the first element.

    # Case 3: Multiple colors, and the largest object exists
    elif largest_obj_color != -1:
        bbox = get_object_bounding_box(largest_obj_coords)

        #If 2, 5 exists, try to extract a subgrid
        if largest_obj_color == 5 and 2 in objects:

          # Search within largest object bounding box

          for r in range(bbox[0], bbox[2] + 1):
              for c in range(bbox[1], bbox[3]+ 1):

                  if input_grid[r][c] == 2 or input_grid[r][c] == 5:
                      output_grid = []

                      try:
                          # extract a 2 x 2 grid starting at [r][c]
                          for i in range(2):
                              row = []
                              for j in range(2):
                                  row.append(input_grid[r+i][c+j])
                              output_grid.append(row)

                          output_grid_np = np.array(output_grid)
                          if 2 in output_grid_np and 5 in output_grid_np:

                                return output_grid
                      except:
                          pass # Try next position

        return [[-1]] #Return Invalid Output (-1)
    else:
        return [[-1]] #Return Invalid Output (-1)
```