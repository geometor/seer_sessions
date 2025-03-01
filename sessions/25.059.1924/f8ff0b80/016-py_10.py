"""
Identifies objects in the input grid. If there's only one object, the output is identical to the input. If there are multiple objects that form a specific pattern (vertical lines in two columns), rearrange them while preserving their relative positions and applying a y-offset. Otherwise, the output is the same as the input
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions (objects) of the same color in a grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                objects.append({'color': grid[row, col], 'pixels': object_pixels})
    return objects

def detect_vertical_line_pattern(objects):
    """
    Detects if the objects form a specific vertical line pattern.
    """
    if len(objects) != 3:
        return False

    # Check if all objects are vertical lines (simplified check)
    for obj in objects:
        pixels = obj['pixels']
        cols = [p[1] for p in pixels]
        if len(set(cols)) > 2:  # Assuming a line has a small number of unique columns
            return False

    # Check for two-column arrangement (simplified check)
    all_pixels = [p for obj in objects for p in obj['pixels']]
    cols = sorted(list(set([p[1] for p in all_pixels])))
    
    if len(cols) != 4:
        return False

    # Check for alternating colors
    obj1_cols = sorted(list(set([p[1] for p in objects[0]['pixels']])))
    obj2_cols = sorted(list(set([p[1] for p in objects[1]['pixels']])))
    obj3_cols = sorted(list(set([p[1] for p in objects[2]['pixels']])))
    
    if obj1_cols[0] != obj2_cols[0] or obj2_cols[0] != obj3_cols[0]:
        return False
      
    if obj1_cols[1] != obj2_cols[1] or obj2_cols[1] != obj3_cols[1]:
      return False

    return True

def apply_vertical_line_transformation(input_grid, objects):
  """Applies the specific transformation for the vertical line pattern."""
  output_grid = np.copy(input_grid)

  y_offset = 0
  if len(objects) > 1:
      # Calculate the y-offset
      first_object_top = min(p[0] for obj in objects for p in obj['pixels'])
      y_offset = -1

  # Create new pixel positions for the vertical lines:
  for obj in objects:
    new_pixels = []
    for r, c in obj['pixels']:
        new_pixels.append((r + y_offset, c))
        output_grid[r,c] = 0  # clear the old entry

    obj['pixels'] = new_pixels

  # copy them to the new grid
  for obj in objects:
    for r, c in obj['pixels']:
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
        output_grid[r,c] = obj['color']


  return output_grid

def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(np.array(input_grid))

    # If only one object, return the input grid unchanged
    if len(objects) <= 1:
        return input_grid

    # Detect the vertical line pattern
    if detect_vertical_line_pattern(objects):
        # Apply the specific transformation for the vertical line pattern
        return apply_vertical_line_transformation(input_grid, objects)
    else:
        #If the pattern is not found, return original
        return input_grid