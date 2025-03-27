```python
"""
1.  **Object Identification:** Identify all distinct objects in the input grid. An object is a contiguous set of pixels of the same non-zero color. Record the color and shape (coordinates) of each object.

2.  **Azure Object Reflection:** For each object with color azure (8):
    *   Create a reflected copy of the object. The reflected object's position is determined by mirroring its coordinates across the grid's vertical center line.  The reflected copy has same color as original.
    *   Keep the original azure colored object.

3.  **Non-Azure Object Transformation and Insertion:**
    * For each row in the grid and for each non-azure, non-white object in that row:
        *  Find the number of distinct azure objects to the left of the center column.  Insert one pixel of this non-azure object's color to the left of the center by the number of azure objects on that side. The inserted pixel's row is the same as the row of object being processed. The column is calculated to maintain the appropriate distance from the center.
        *  Find the number of distinct azure objects to the right of the center column (inclusive of center if width is odd). Insert one pixel of this object's color, mirrored horizontally, to the right of the center by the number of azure objects to that side.  The inserted pixel's row is the same as the row of the object being processed.

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

def count_azure_objects(grid, row, center_col, is_odd):
    """Counts azure objects to the left and right of the center."""
    rows, cols = grid.shape
    left_count = 0
    right_count = 0
    visited = set()

    # Count distinct azure objects to the left
    for c in range(center_col):
        if grid[row, c] == 8 and (row, c) not in visited:
            left_count += 1
            # DFS to mark the entire object as visited
            stack = [(row, c)]
            while stack:
                cr, cc = stack.pop()
                if (cr, cc) not in visited and 0 <= cr < rows and 0 <= cc < cols and grid[cr,cc] == 8:
                    visited.add((cr,cc))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        stack.append((cr+dr, cc+dc))

    # Count distinct azure objects to the right
    for c in range(center_col + (1 if is_odd else 0), cols):
        if grid[row, c] == 8 and (row, c) not in visited:
            right_count += 1
             # DFS to mark the entire object as visited
            stack = [(row, c)]
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

    # Reflect azure objects and keep original
    for color, obj_coords in objects:
        if color == 8:  # azure
             for r, c in obj_coords:
                output_grid[r, c] = color  # Keep original
             reflected_coords = reflect_object(obj_coords, cols)
             for r, c in reflected_coords:
                output_grid[r, c] = color  # Add reflection

    # Insert pixels based on azure object counts
    for color, obj_coords in objects:
      if color != 8 and color != 0: # non-azure, non-white
        obj_rows = sorted(list(set([r for r, c in obj_coords])))
        for row in obj_rows:
          left_azure_count, right_azure_count = count_azure_objects(input_grid, row, center_col, is_odd)

          # Insert to the left
          insert_col_left = center_col - 1 - left_azure_count
          if insert_col_left >= 0:
              output_grid[row, insert_col_left] = color

          # Insert to the right
          insert_col_right = center_col + (1 if is_odd else 0) + right_azure_count -1
          if insert_col_right < cols :
              output_grid[row, insert_col_right] = color

    return output_grid
```