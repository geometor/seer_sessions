"""
1.  **Identify Objects:** Locate all contiguous regions of yellow (4) pixels and isolated gray (5) pixels within the input grid.
2.  **Preserve Gray Pixels:** The positions of the isolated gray (5) pixels remain unchanged in the output grid.
3.  **Expand Yellow Region:** The yellow (4) region expands outwards in all directions (up, down, left, and right).
4. **Expansion Rules:**
    *   The yellow pixels expand one layer at a time.
    *   The expansion happens until the yellow region takes the maximum possible area.
    *   The expansion happens around any white space (0) but does not go over other colors.
5.  **Output:** The resulting grid after performing the expansion and preserving gray pixel locations represents the transformation.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = set()

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_object):
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != color:
            return
        visited.add((x, y))
        current_object.append((x, y))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(x + dx, y + dy, current_object)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and (x, y) not in visited:
                current_object = []
                dfs(x, y, current_object)
                objects.append(current_object)
    return objects

def find_isolated_pixels(grid, color):
  """
  Find isolated pixels in the grid
  """
  isolated = []
  for r in range(grid.shape[0]):
      for c in range(grid.shape[1]):
          if grid[r,c] == color:
            is_isolated = True
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                            if grid[nr,nc] == color:
                                is_isolated = False
                                break
                if not is_isolated:
                    break
            if is_isolated:
              isolated.append((r,c))
  return isolated
                                
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find isolated gray pixels
    gray_pixels = find_isolated_pixels(input_grid, 5)
    
    # find yellow objects
    yellow_objects = find_objects(input_grid, 4)

    # expand yellow region
    if yellow_objects:
      expanded_yellow = set()
      for obj in yellow_objects:
        for x,y in obj:
          expanded_yellow.add((x,y))
      
      while True:
          new_expanded_yellow = set(expanded_yellow)
          for x, y in expanded_yellow:
              for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                  nx, ny = x + dx, y + dy
                  if 0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1] and input_grid[nx,ny] == 0:
                        new_expanded_yellow.add((nx, ny))
          if new_expanded_yellow == expanded_yellow:
            break;
          else:
            expanded_yellow = new_expanded_yellow

      for x,y in expanded_yellow:
          output_grid[x,y] = 4
    
    # preserve gray pixels by setting after, in case expansion went over them
    for x, y in gray_pixels:
        output_grid[x, y] = 5

    return output_grid