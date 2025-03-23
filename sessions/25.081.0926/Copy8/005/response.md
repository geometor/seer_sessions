```python
"""
1. Identify Objects: Find all contiguous regions of non-zero (non-white) pixels.
2. Conditional Duplication:
    *  Example 1: If an object spans multiple rows and its shape is not simply vertical, then it may be targeted for action. The object with color 2 is targeted. Duplicate the entire targeted object, and position the copy so its left-most edge aligns with the left most edge of any other object in the input grid. The duplicated object will overlap any existing object.
    *  Example 2: Single pixel objects are duplicated *horizontally* to fill available empty (0-colored) spaces that are adjacent to an existing object. The duplicated pixels of an object are of the same color and always adjacent.

3. Preservation:  The original objects are mostly preserved (though they can be overlapped). Only in Example 2 are new objects created through expansion into blank spaces.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and returns a list of objects in the grid.
    Each object is represented by a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape
    
    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] == 0:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append((grid[r,c],current_object)) # save value with the object
    return objects

def is_single_pixel_object(obj):
    """Checks if an object is a single pixel."""
    return len(obj) == 1

def get_object_bounds(obj):
    """Gets the bounding box of an object."""
    rows, cols = zip(*obj)
    return min(rows), max(rows), min(cols), max(cols)


def transform(input_grid):
    """
    Transforms the input grid based on the observed rules.
    """
    output_grid = np.copy(input_grid)
    objects = get_objects(input_grid)
    rows, cols = input_grid.shape

    # Example 1 style duplication
    for color, obj in objects:
        min_row, max_row, min_col, max_col = get_object_bounds(obj)
        if (max_row - min_row + 1) > 1 and (max_col - min_col + 1) >1 :  # Not a single row or single pixel object
            # Find leftmost column of any object
            target_col = min(o_min_col for _, other_obj in objects for _, _, o_min_col, _ in [get_object_bounds(other_obj)] )

            #Duplicate and shift
            col_offset = target_col - min_col
            if col_offset != 0:
                for row, col in obj:
                    new_col = col + col_offset
                    if 0 <= new_col < cols: #check new col is in bounds
                       output_grid[row,new_col] = color

    # Example 2 style duplication (single-pixel horizontal expansion)
    for color, obj in objects:
      if is_single_pixel_object(obj):
          row, col = obj[0]

          # Check right neighbor
          if col + 1 < cols and output_grid[row, col + 1] == 0:
              # find nearest non-zero object horizontally
              found_neighbor = False
              for other_color, other_obj in objects:
                if other_color != 0:
                  for o_row, o_col in other_obj:
                    if o_row == row and o_col > col:
                      found_neighbor = True
                      break
                if found_neighbor: break

              if found_neighbor:
                output_grid[row, col + 1] = color

    return output_grid
```