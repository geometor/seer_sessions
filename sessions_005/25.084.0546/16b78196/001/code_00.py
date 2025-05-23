"""
The transformation rule involves identifying rectangular objects of different colors and sizes within the grid,
and then applying color changes when small colored blocks are positioned beside larger solid rectangles.
The output grid maintains the overall structure but reflects these interactions, primarily color updates.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies rectangular objects in the grid.
    Returns a list of dictionaries, each representing an object.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                color = grid[r, c]
                # Find object boundaries
                r_end = r
                while r_end < rows and grid[r_end, c] == color:
                    r_end += 1
                c_end = c
                while c_end < cols and grid[r, c_end] == color:
                    c_end += 1

                # Check if it's a valid rectangle
                valid_rectangle = True
                for i in range(r, r_end):
                    for j in range(c, c_end):
                        if grid[i, j] != color:
                            valid_rectangle = False
                            break
                    if not valid_rectangle:
                        break

                if valid_rectangle:
                    objects.append({
                        'color': color,
                        'start_row': r,
                        'end_row': r_end,
                        'start_col': c,
                        'end_col': c_end
                    })
                    # Mark as visited
                    visited[r:r_end, c:c_end] = True
    return objects

def is_adjacent(obj1, obj2):
    """Checks if two objects are adjacent (including diagonals)."""
    return not (obj1['end_row'] < obj2['start_row'] or
                obj1['start_row'] > obj2['end_row'] or
                obj1['end_col'] < obj2['start_col'] or
                obj1['start_col'] > obj2['end_col'])

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Find the large object, if any
    large_object = None
    for obj in objects:
      height = obj['end_row'] - obj['start_row']
      if height > 4: #this distinguishes "large"
        large_object = obj
        break
        
    if large_object is None:
       return output_grid

    # Iterate through other objects
    for obj in objects:
      if obj is not large_object:
        height = obj['end_row'] - obj['start_row']
        width = obj['end_col'] - obj['start_col']
        if height == 1 and width == 1:
          # this is a 1 pixel object - check it's neighbors
          for r in range(obj['start_row'] - 1, obj['end_row'] + 1):
            for c in range(obj['start_col'] - 1, obj['end_col'] + 1):
              if (r >= large_object['start_row'] and r < large_object['end_row']
                  and c >= large_object['start_col'] and c < large_object['end_col']
                  and (r != obj['start_row'] or c != obj['start_col'])):
                  output_grid[r, c] = obj['color']

    return output_grid