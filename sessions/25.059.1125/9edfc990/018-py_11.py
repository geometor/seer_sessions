"""
1.  **Identify Objects:**  Identify all distinct objects in the input grid. An object is a group of connected pixels of the same color.
2.  **Compare Objects:** For each input object find the matching object in the output object by location.
3.  **Determine Color Change**:  If the color changed to blue, then change that object in the input to blue.
4.  **Output:** Return the modified grid.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    An object is a group of connected pixels of the same color.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_id):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        objects[object_id].append((row, col))
        dfs(row + 1, col, color, object_id)
        dfs(row - 1, col, color, object_id)
        dfs(row, col + 1, color, object_id)
        dfs(row, col - 1, color, object_id)

    object_count = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_id = f"object_{object_count}"
                objects[object_id] = []
                dfs(row, col, color, object_id)
                object_count += 1
    return objects

def get_object_center(object_pixels):
    """Calculates the center (centroid) of an object."""
    rows = [p[0] for p in object_pixels]
    cols = [p[1] for p in object_pixels]
    center_row = int(np.mean(rows))
    center_col = int(np.mean(cols))
    return (center_row, center_col)

def transform(input_grid, output_grid):
    # initialize output_grid
    output_grid_copy = np.copy(input_grid)

    # find the objects
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    # Compare objects and determine color change
    for input_object_id, input_pixels in input_objects.items():
      input_color = input_grid[input_pixels[0]]

      # find the object center to match
      input_center = get_object_center(input_pixels)

      # locate output_object my matching center
      output_object_found = False
      for output_object_id, output_pixels in output_objects.items():
          output_center = get_object_center(output_pixels)
          if input_center == output_center:
            #found matching object
            output_color = output_grid[output_pixels[0]]
            if output_color == 1:
              # found blue, make object blue
              for row,col in input_pixels:
                output_grid_copy[row,col] = 1
            output_object_found = True
            break

    return output_grid_copy