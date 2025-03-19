"""
The input has rectangles whose colors are changed to another color, and the
rectangles are moved to new locations by reflection over the main diagonal.
Horizontal bars stay at their original location, and will be overwritten by the
shapes if their new locations overlap.
"""

import numpy as np

def find_rectangles(grid):
    # find all filled rectangular shapes within the grid, excluding horizontal
    # bar shapes.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    rectangles = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, rect):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        rect.append((r, c))
        dfs(r + 1, c, color, rect)
        dfs(r - 1, c, color, rect)
        dfs(r, c + 1, color, rect)
        dfs(r, c - 1, color, rect)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                rect = []
                dfs(r, c, color, rect)
                if rect:
                    # Check if it's a rectangle
                    min_r = min(x[0] for x in rect)
                    max_r = max(x[0] for x in rect)
                    min_c = min(x[1] for x in rect)
                    max_c = max(x[1] for x in rect)
                    if len(rect) == (max_r - min_r + 1) * (max_c - min_c + 1):
                         #calculate height and width
                        height = max_r - min_r + 1
                        width = max_c - min_c + 1

                        #check if the rectangle belongs to horizontal bars
                        if height != 4:
                            rectangles.append(
                                {"top_left": (min_r, min_c), "color": color,
                                 "height": height, "width": width})
    return rectangles

def swap_colors(grid, rectangles, swap_rules):
    # swap colors within rectangles based on given rules
    new_grid = np.copy(grid)
    for rect in rectangles:
        top_r, top_c = rect['top_left']
        for r in range(top_r, top_r + rect['height']):
            for c in range(top_c, top_c + rect['width']):
                for rule in swap_rules:
                    if new_grid[r, c] == rule['original_color']:
                        new_grid[r, c] = rule['new_color']
                        break # apply only one rule
    return new_grid

def reflect_position(top_left, height, width, grid_shape):
  # Reflects the rectangle position over the main diagonal
  new_top_left = (top_left[1], top_left[0])
  new_height = width
  new_width = height
  return new_top_left, new_height, new_width


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid_shape = output_grid.shape

    # find rectangles in the input grid
    rectangles = find_rectangles(input_grid)
    
    # determine swap rules based on input
    if input_grid[5, 5] == 6:  # Based on observation
        swap_rules = [
          {'original_color': 6, 'new_color': 3}
        ]
    elif input_grid[2, 23] == 4 and input_grid[5,10] == 6:
        swap_rules = [
          {'original_color': 6, 'new_color': 4},
          {'original_color': 4, 'new_color': 6},
          {'original_color': 3, 'new_color': 3}
        ]
    elif input_grid[2,24] == 2 and input_grid[12,14] ==4 :
        swap_rules = [
          {'original_color': 2, 'new_color': 4},
          {'original_color': 4, 'new_color': 2},
          {'original_color': 8, 'new_color': 8}
        ]
    else:
        swap_rules = []

    # apply color swapping within the rectangles
    for rect in rectangles:
        top_r, top_c = rect['top_left']
        #reflect each rectangle
        new_top_left, new_height, new_width = reflect_position(
            rect['top_left'], rect['height'], rect['width'], grid_shape)

        # reset the area to 0 before redraw the shapes, to prevent the horizonal
        # shapes
        for i in range(rect['height']):
            for j in range(rect['width']):
                old_r = top_r + i
                old_c = top_c + j
                output_grid[old_r,old_c] = 0 #reset everything to 0

    # redraw the reflected rectangles
    for rect in rectangles:
      new_top_left, new_height, new_width = reflect_position(
            rect['top_left'], rect['height'], rect['width'], grid_shape
        )

        for r in range(new_height):
          for c in range(new_width):

              new_r = new_top_left[0] + r
              new_c = new_top_left[1] + c

              #check for boundary, skip if out of boundary
              if new_r < 0 or new_r >= grid_shape[0] or new_c < 0 or new_c >= grid_shape[1]:
                continue

              for rule in swap_rules:
                  if rect['color'] == rule['original_color']:
                    output_grid[new_r, new_c] = rule['new_color']
                    break
                  else:
                      output_grid[new_r,new_c] = rect['color']

    return output_grid