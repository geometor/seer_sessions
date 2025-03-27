"""
1.  **Object Identification:** Identify all distinct objects in the input grid. An object is a contiguous set of pixels of the same non-zero color. Record the color and shape (coordinates) of each object.

2.  **Azure Object Reflection:** For each object with color azure (8):
    *   Create a reflected copy of the object. The reflected object's position is determined by mirroring its coordinates across the grid's vertical center line.  The reflected copy has same color as original.
    *   Keep the original azure colored object.

3.  **Non-Azure Object Transformation and Insertion:**
    *   Iterate through each *row* of the input grid.
    *   For each non-azure, non-white object *found in that row*:
        *   Count the number of distinct azure objects to the *left* of the center column in the *entire grid*.
        *   Insert a single pixel of the object's color to the left of the center column, at a distance equal to the count of left-side azure objects. The row of insertion is the same as the row being iterated.
        *   Count the number of distinct azure objects to the *right* of the center column (including the center column if the grid width is odd) in the *entire grid*.
        *   Insert a single pixel of the object's color to the right of the center, at a distance equal to the right-side azure objects count. The row of insertion is the same as the row being iterated.

4.  **Output Construction:** Create the output grid by placing all original azure objects, reflected azure objects, and inserted pixels onto a blank grid of the same dimensions as the input. All other cells become white.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of the same color in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r,c] != 0:
                color = grid[r, c]
                obj = []
                dfs(r, c, color, obj)
                objects.append((color, obj))
    return objects

def reflect_object(obj, width):
    """Reflects an object horizontally across the center of the grid."""
    reflected_obj = []
    for r, c in obj:
        reflected_c = width - 1 - c
        reflected_obj.append((r, reflected_c))
    return reflected_obj

def count_all_azure_objects(grid):
    """Counts azure objects to the left and right of the center in entire grid"""
    rows, cols = grid.shape
    center_col = cols // 2
    is_odd = cols % 2 != 0
    left_count = 0
    right_count = 0
    visited = set()

     # Count distinct azure objects to the left
    for r in range(rows):
      for c in range(center_col):
          if grid[r, c] == 8 and (r, c) not in visited:
              left_count += 1
              # DFS to mark the entire object as visited
              stack = [(r, c)]
              while stack:
                  cr, cc = stack.pop()
                  if (cr, cc) not in visited and 0 <= cr < rows and 0 <= cc < cols and grid[cr,cc] == 8:
                      visited.add((cr,cc))
                      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                          stack.append((cr+dr, cc+dc))

    # Count distinct azure objects to the right
    for r in range(rows):
      for c in range(center_col + (1 if is_odd else 0), cols):
          if grid[r, c] == 8 and (r, c) not in visited:
              right_count += 1
               # DFS to mark the entire object as visited
              stack = [(r, c)]
              while stack:
                  cr, cc = stack.pop()
                  if (cr, cc) not in visited and 0 <= cr < rows and 0 <= cc < cols and grid[cr,cc] == 8:
                      visited.add((cr,cc))
                      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                          stack.append((cr+dr, cc+dc))
    return left_count, right_count

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    center_col = cols // 2
    is_odd = cols % 2 != 0

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Reflect azure objects
    for color, obj_coords in objects:
        if color == 8:  # azure
            for r, c in obj_coords:
                output_grid[r, c] = color # Keep original object
            reflected_coords = reflect_object(obj_coords, cols)
            for r, c in reflected_coords:
                output_grid[r, c] = color  # Add reflection

    left_azure_count, right_azure_count = count_all_azure_objects(input_grid)

    # Iterate through each row
    for row in range(rows):
        # Find non-azure, non-white objects in the current row
        row_objects = []
        for color, obj_coords in objects:
            if color != 8 and color != 0:
              for r,c in obj_coords:
                if r == row:
                  row_objects.append((color, obj_coords))
                  break # only consider one instance per object

        for color, obj_coords in row_objects:

            # Insert to the left
            insert_col_left = center_col - 1 - left_azure_count
            if insert_col_left >= 0:
                output_grid[row, insert_col_left] = color

            # Insert to the right
            insert_col_right = center_col + (1 if is_odd else 0) + right_azure_count -1
            if insert_col_right < cols:
                output_grid[row, insert_col_right] = color

    return output_grid