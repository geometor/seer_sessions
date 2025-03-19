"""
The transformation rule is:  Identify the maroon (color 9) object located in the bottom-right corner of the input grid. Change the color of this object to grey (color 5) in the output grid. All other parts of the grid remain unchanged. The size and shape of the object may vary, but is must be in the bottom-right.
"""

import numpy as np

def find_bottom_right_object(grid, color):
    # Find the coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Object of specified color not found

    # Find the bottom-rightmost coordinate.
    bottom_right_coord = coords[np.argmax(coords[:, 0] + coords[:, 1])]


    # Use flood fill to find connected component
    object_coords = []
    visited = set()
    queue = [tuple(bottom_right_coord)]

    while queue:
      curr = queue.pop(0)
      if curr in visited:
        continue
      visited.add(curr)

      if grid[curr] == color:
        object_coords.append(curr)
        row, col = curr

        # explore neighbors
        neighbors = [(row-1,col),(row+1,col),(row,col-1),(row,col+1)]

        for r,c in neighbors:
          if (0 <= r < grid.shape[0]) and (0 <= c < grid.shape[1]):
              queue.append((r,c))

    if not object_coords:
      return None
    
    object_coords = np.array(object_coords)
    min_row = np.min(object_coords[:, 0])
    max_row = np.max(object_coords[:, 0])
    min_col = np.min(object_coords[:, 1])
    max_col = np.max(object_coords[:, 1])

    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the maroon object (color 9) at the bottom-right.
    maroon_object_coords = find_bottom_right_object(input_grid, 9)

    # If a maroon object is found at the bottom-right, change its color to grey (5).
    if maroon_object_coords:
        min_row, max_row, min_col, max_col = maroon_object_coords
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if output_grid[row, col] == 9:  # ensure we are changing correct cells
                  output_grid[row, col] = 5

    return output_grid