"""
The transformation replaces the border of the Green regions and the yellow pixels within them with grey, and relocates a composite object (structure_1).
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
          if grid[x,y+1] == 6 and grid[x, y-1] == 6:
            top_left = (x-1,y)
            pixels = [(top_left[0], top_left[1]), (top_left[0], top_left[1]+1), (top_left[0], top_left[1]+2),
            (top_left[0]+1, top_left[1]), (top_left[0]+1, top_left[1]+1), (top_left[0]+1, top_left[1]+2),
            (top_left[0]+2, top_left[1]), (top_left[0]+2, top_left[1]+1), (top_left[0]+2, top_left[1]+2)]

            colors = [grid[px,py] for px, py in pixels]
            if all(c in [5,6,4] for c in colors):
              return pixels
    return []

def move_structure(grid, structure, region):
    # Move structure to region.
    min_x = min([x for x, y in region])
    max_x = max([x for x, y in region])
    min_y = min([y for x, y in region])
    max_y = max([y for x, y in region])

    struct_height = max([x for x,y in structure]) - min([x for x,y in structure]) + 1
    struct_width = max([y for x,y in structure]) - min([y for x,y in structure]) + 1

    new_x = min_x + 1
    new_y = min_y + 1

    if new_x + struct_height > max_x:
        new_x = max_x - struct_height -1
    
    if new_y + struct_width > max_y:
        new_y = max_y - struct_width - 1

    structure_origin = structure[0]

    moved_structure = [(x - structure_origin[0] + new_x, y - structure_origin[1] + new_y) for x,y in structure ]

    return moved_structure

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find green regions
    green_regions = find_objects(input_grid, 3)

    #find the structure
    structure = find_structure(input_grid)


    # Iterate through each green region
    for region in green_regions:
      #find and move structure
      if len(structure) > 0:

        moved_struct = move_structure(input_grid, structure, region)
        #clean old structure position
        for x, y in structure:
          output_grid[x,y] = input_grid[x,y]

        #paint in new position
        color_struct = [input_grid[x,y] for x,y in structure]

        for i, pos in enumerate(moved_struct):
            output_grid[pos] =  color_struct[i]


      # Get the border pixels of the current region
      border = get_border(region, input_grid.shape)

      # Replace yellow border pixels with grey, and the rest with grey.
      for x, y in border:
          if input_grid[x,y] == 4:
            output_grid[x,y] = 5
          else:
            output_grid[x,y] = 5

    return output_grid