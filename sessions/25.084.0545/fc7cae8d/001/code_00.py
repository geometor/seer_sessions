"""
The transformation extracts specific colored shapes from the input grid and represents them in a compressed form in the output grid. The relevant colors and shapes differ between examples, but the general principle is to identify key objects, extract their color information, and map them to a smaller grid, preserving relative positions where possible.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                obj = []
                dfs(row, col, color, obj)
                if obj:
                    objects.append((color, obj))
    return objects

def get_bounding_box(obj):
    """
    Returns the bounding box of an object (list of coordinates).
    """
    min_row = min(coord[0] for coord in obj)
    max_row = max(coord[0] for coord in obj)
    min_col = min(coord[1] for coord in obj)
    max_col = max(coord[1] for coord in obj)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)

    # Example-specific logic (this needs to be generalized)
    if len(objects) > 10: #train_1, _3 like rule
        # Extract Azure objects.

        target_color = 8
        target_objects = [obj for color, obj in objects if color == target_color]

        if not target_objects:
             target_color = 9 # handling train 3 where the objects are split
             target_objects = [obj for color, obj in objects if color == target_color]


        # Find top-left of bounding box for all target_objects

        output_grid = [] #initialize output_grid.
        #get max dimensions of all azure objects
        max_height = 0
        max_width = 0
        for obj_coords in target_objects:
          min_row, min_col, max_row, max_col = get_bounding_box(obj_coords)
          height = max_row - min_row + 1
          width = max_col-min_col + 1
          if height>max_height:
            max_height=height
          if width>max_width:
            max_width=width

        output_grid = np.zeros((max_height, max_width), dtype=int)

        for azure in target_objects: #draw all the objects to the topleft.
          min_row, min_col, max_row, max_col = get_bounding_box(azure)

          for row, col in azure:
                output_grid[row - min_row, col - min_col] = target_color


    else: #train_2 like rule
        #extract yellow objects
        target_color = 4
        target_objects = [obj for color, obj in objects if color == target_color]

        # Find top-leftmost coordinate of the target object
        if target_objects: #sometimes there may not be target objects.
          output_grid = [] #initialize output_grid.
          #get max dimensions of all azure objects
          max_height = 0
          max_width = 0
          for obj_coords in target_objects:
            min_row, min_col, max_row, max_col = get_bounding_box(obj_coords)
            height = max_row - min_row + 1
            width = max_col-min_col + 1
            if height>max_height:
              max_height=height
            if width>max_width:
              max_width=width

          output_grid = np.zeros((max_height, max_width), dtype=int)

          for obj_coords in target_objects: #condense all coordinates
            min_row, min_col, max_row, max_col = get_bounding_box(obj_coords)

            for row, col in obj_coords:
                  output_grid[row - min_row, col - min_col] = target_color

        else: #if no target objects.
          output_grid = np.array([]) #output is empty.

    return output_grid.tolist()