"""
1. **Find Green Regions:** Identify all contiguous regions of green (3) pixels.
2. **Process Border:** Iterate through the border pixels of each green region and replace the border with grey ONLY if it is yellow color.
3. **Identify Structure:** Find a specific 3x3 structure. The structure is identifiable by its color arrangement. It consists of gray pixels on left and right adjacent to a magenta center pixel.
4. **Remove Structure:** Remove the identified structure entirely from the grid, turning the structure pixels to white (background color is assumed).
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y):
        if not is_valid(x, y) or visited[x, y] or grid[x, y] != color:
            return []

        visited[x, y] = True
        object_pixels = [(x, y)]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            object_pixels.extend(dfs(x + dx, y + dy))

        return object_pixels

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and not visited[x, y]:
                objects.append(dfs(x, y))

    return objects

def get_border(pixels, grid_shape):
    border_pixels = []
    for x, y in pixels:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < grid_shape[0] and 0 <= ny < grid_shape[1]):
               continue

            if (nx, ny) not in pixels:
                border_pixels.append((x,y))
                break
    return border_pixels

def find_structure(grid):
    # find the structure
    for x in range(grid.shape[0]):
      for y in range(grid.shape[1]):
        if grid[x,y] == 5:
          if y + 1 < grid.shape[1] and y - 1 >= 0:
            if grid[x,y+1] == 6 and grid[x, y-1] == 6:
              top_left = (x-1,y-1)
              pixels = [(top_left[0], top_left[1]), (top_left[0], top_left[1]+1), (top_left[0], top_left[1]+2),
              (top_left[0]+1, top_left[1]), (top_left[0]+1, top_left[1]+1), (top_left[0]+1, top_left[1]+2),
              (top_left[0]+2, top_left[1]), (top_left[0]+2, top_left[1]+1), (top_left[0]+2, top_left[1]+2)]

              valid_struct = True

              for px, py in pixels:
                if not (0 <= px < grid.shape[0] and 0 <= py < grid.shape[1]):
                  valid_struct = False
                  break
              
              if valid_struct:
                return pixels
    return []


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find green regions
    green_regions = find_objects(input_grid, 3)

    #find the structure
    structure = find_structure(input_grid)

    # Iterate through each green region
    for region in green_regions:
      # Get the border pixels of the current region
      border = get_border(region, input_grid.shape)

      # Replace yellow border pixels with grey.
      for x, y in border:
          if input_grid[x,y] == 4:
            output_grid[x,y] = 5


    # Remove structure
    if len(structure) > 0:
        for x, y in structure:
            output_grid[x, y] = 0  # Assuming 0 is the background color

    return output_grid