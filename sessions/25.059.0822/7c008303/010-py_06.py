"""
The transformation extracts specific color blocks from the input grid to form the output grid.
Azure and Green color pixels are completely removed. Blue, Red, and Yellow in the top-right
corner are extracted and rearranged in the output grid. Remaining pixels are filled with white.
"""

import numpy as np

def find_objects(grid, colors):
    """Find objects of specified colors in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] in colors:
                obj = []
                stack = [(r, c)]
                visited[r, c] = True

                while stack:
                    curr_r, curr_c = stack.pop()
                    obj.append((curr_r, curr_c))

                    neighbors = [
                        (curr_r - 1, curr_c),
                        (curr_r + 1, curr_c),
                        (curr_r, curr_c - 1),
                        (curr_r, curr_c + 1),
                    ]
                    for nr, nc in neighbors:
                        if (
                            0 <= nr < rows
                            and 0 <= nc < cols
                            and not visited[nr, nc]
                            and grid[nr, nc] == grid[r, c]
                        ):
                            stack.append((nr, nc))
                            visited[nr, nc] = True
                objects.append(obj)
    return objects

def extract_top_right_br(input_grid):
  """Extracts blue and red object from top-right corner"""
  rows, cols = input_grid.shape
  for r in range(rows):
    for c in range(cols):
      if input_grid[r,c] == 1 or input_grid[r,c] == 2:
        return find_objects(input_grid, [1, 2])
  return []

def extract_top_right_y(input_grid):
    """Extracts the yellow object from top right that is in contact with blue"""
    blue_red_object = extract_top_right_br(input_grid)
    blue_object = [(r,c) for (r,c) in blue_red_object[0] if input_grid[r,c] == 1]
    
    yellow_object = []
    rows, cols = input_grid.shape
    for (br,bc) in blue_object:
        neighbors = [
                        (br - 1, bc),
                        (br + 1, bc),
                        (br, bc - 1),
                        (br, bc + 1),
                    ]
        for (nr, nc) in neighbors:
                if (0 <= nr < rows and 0 <= nc < cols and input_grid[nr,nc] == 4 ):
                    yellow_object.append((nr, nc))
                    

    return yellow_object
    

def transform(input_grid):
    """Transforms the input grid to the output grid."""
    input_grid = np.array(input_grid)

    # Extract blue and red object from top-right
    blue_red_object = extract_top_right_br(input_grid)[0]
   
    # Extract yellow object from top right that is in contact with blue
    yellow_object = extract_top_right_y(input_grid)
   
    # Initialize output grid with zeros (white)
    output_grid = np.zeros((6, 6), dtype=int)

    # Place the blue and red object pixels
    for r, c in blue_red_object:
      # calculate the destination of these pixels
      if input_grid[r,c] == 1: #blue
        dr, dc = r, c-7   # relative location
        if 0 <= dr < 6 and 0 <= dc < 6: # check boundaries
           output_grid[dr, dc] = 1 # set to blue
      elif input_grid[r,c] == 2:
        dr, dc = r, c-4    # relative location
        if 0 <= dr < 6 and 0 <= dc < 6:
            output_grid[dr, dc] = 2   # set to red

    # Place yellow pixels
    for r,c in yellow_object:
       dr, dc = r-4, c-6   # relative location
       if 0 <= dr < 6 and 0 <= dc < 6:
          output_grid[dr,dc] = 4


    return output_grid