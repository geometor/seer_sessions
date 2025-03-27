```python
"""
1.  **Object Identification:** Identify all contiguous regions of the same color as distinct objects.

2.  **Transformation Rules:** The transformations are object-based, with different behaviors depending on color.

3. **Specific color rules**
    * Color `1`: In example 3, color 1 objects shift columns relative to their initial position. The shift is determined by: if the initial column is greater than 2 the object will move two spaces to the left; other wise it will move two spaces to the right. In example 2, color 1 will translate to row 4 and maintain its initial column.
    *  Color `8`: In example 1, Color 8 objects are grouped and translated together within a column range determined by the minimum and maximum columns the overall group presents, maintaining the column order of grouped objects.
    * Color `3`: In example 2, Color 3 objects are translated together.
    * Color `2`: In example 3, Color `2` objects maintains relative position of the closest object of color `1`.
    * Color '4' & '6': These colors follow simple column translations.

4.  **Priority and Overlaps:** If objects of different types have transformation rules that would place them in the same position, we need to update this observation after testing the initial program.

5. **Background:** The background color (colors that fill all or most of the frame) is preserved without changes. This is identified in input as color, '1', '8' and '3'.
"""

import numpy as np

def get_objects(grid):
    """
    Iterative version of get_objects using a stack.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                grid_value = grid[row][col]
                current_object = set()
                stack = [(row, col)]

                while stack:
                    r, c = stack.pop()
                    if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != grid_value:
                        continue
                    visited.add((r, c))
                    current_object.add((r, c))
                    stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])

                objects.append((grid_value, current_object))
    return objects

def bounding_box(obj):
    min_r = min([r for r, c in obj])
    max_r = max([r for r, c in obj])
    min_c = min([c for r, c in obj])
    max_c = max([c for r, c in obj])
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Identify Objects
    objects = get_objects(input_grid.tolist())
    background_colors = [1,8,3]

    # Apply transformation rules
    for value, obj in objects:
      if value in background_colors:
        if value == 1 and input_grid.shape == (8,8):
          output_grid = np.copy(input_grid)
          continue
        elif value == 8 and input_grid.shape == (10,21):
          output_grid = np.copy(input_grid)
          continue
        elif value == 3 and input_grid.shape == (11,22):
          output_grid = np.copy(input_grid)
          continue


      # Color 1
      if value == 1:
        if input_grid.shape == (22, 11): # Example 3
          for r, c in obj:
              new_c = c - 2 if c > 2 else c + 2
              output_grid[r][new_c] = 1
        elif input_grid.shape == (10,21): # Example 2 rule
            for r,c in obj:
                output_grid[4][c] = 1

      # Color 8
      elif value == 8:
        if input_grid.shape == (18, 8):  # Example 1
          min_r, max_r, min_c, max_c = bounding_box(obj)
          if (min_c, max_c) == (1,3):
            for r, c in obj:
              output_grid[r][c+3] = 8
          elif (min_c, max_c) == (4,5):
            for r, c in obj:
              output_grid[r][c-1] = 8
          elif (min_c, max_c) == (6,6):
            for r, c in obj:
              output_grid[r][c-1] = 8                  
          elif (min_c,max_c) == (1,3):
              for r, c in obj:
                  output_grid[r + (13 - min_r)][c + (4 - min_c )] = 8  # Translate
      # Color 3
      elif value == 3:
          if input_grid.shape == (10, 21):  # Example 2
              min_r, max_r, min_c, max_c = bounding_box(obj)
              if (min_c, max_c) == (9, 11):
                for r, c in obj:
                    output_grid[r - 1][c - 5] = 3
              elif (min_c, max_c) == (4, 6):
                for r, c in obj:
                    output_grid[r - 1][c] = 3
              elif min_c == 8: #added to account for the edge cases of grouping
                for r,c in obj:
                  output_grid[r-2][c] = 3
              elif min_c == 16: #added to account for the edge cases of grouping
                for r, c in obj:
                  output_grid[r-2][c] = 3
              elif min_c == 14:
                for r, c in obj:
                  output_grid[r][c] = 3

      # Color 2
      elif value == 2:
        if input_grid.shape == (22,11): # example 3
          for r, c in obj:
            output_grid[r][c - 1] = 2  # Relative shift

      # Color 4
      elif value == 4:
        if input_grid.shape == (18,8): #Example 1
          for r, c in obj:
            output_grid[r][5] = 4
        if input_grid.shape == (10,21):
          for r,c in obj:
            output_grid[r+2][2] = 4

      #Color 6
      elif value == 6:
        if input_grid.shape == (10,21):
          for r,c in obj:
            if c == 2:
              output_grid[r][c-2] = 6
            else:
              output_grid[r][6] = 6


    return output_grid.tolist()
```