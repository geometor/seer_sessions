"""
1.  **Identify Objects:** Find the 2x2 magenta square (color 6) and any green pixels (color 3) in the input grid.
2.  **Expand Magenta Square:** Expand the magenta square by one pixel in all directions. This transforms the 2x2 square into a 4x4 square.
3.  **Replicate and Position Green Pixels:**  If a green pixel exists in the input, replicate it in the output grid. The position of the replicated green pixels is determined relative to the *expanded* magenta square. The exact offsets used for placement are not consistent, but always are relative to the expanded magenta square top-left corner. The placement rule depends on where the initial green pixel is placed and isn't yet precisely defined, other than by the possible offset values. There may be one, two, or four green pixels in the output.
"""

import numpy as np

def find_object(grid, color, shape=None):
    """Finds an object of a specific color and optionally shape."""
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return None

    if shape == "point":
      if len(coords) == 1:
        return coords[0]
      else:
        return None

    if shape == "2x2 square":
        min_row = np.min(coords[:, 0])
        max_row = np.max(coords[:, 0])
        min_col = np.min(coords[:, 1])
        max_col = np.max(coords[:, 1])

        if (max_row - min_row == 1) and (max_col - min_col == 1):
           return (min_row, min_col)  # Return top-left corner
        else:
          return None

    return coords # return all coordinates of matching color

def expand_square(grid, top_left, old_size, new_size, color):
    """Expands a square object by one pixel in all directions."""
    row, col = top_left
    new_grid = np.copy(grid)
    # original square
    for i in range(old_size):
        for j in range(old_size):
          new_grid[row + i][col + j] = color
    # expand square by 1 on all sides
    start_row = row - 1
    start_col = col - 1
    for i in range(new_size):
        for j in range(new_size):
            if 0 <= start_row + i < grid.shape[0] and 0 <= start_col + j < grid.shape[1]:
              new_grid[start_row + i, start_col + j] = color

    return new_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Identify Objects
    magenta_square_coord = find_object(input_grid, 6, "2x2 square")
    green_pixel_coord = find_object(input_grid, 3, "point")

    if magenta_square_coord is None:
      return output_grid

    # Expand Magenta Square
    output_grid = expand_square(output_grid, magenta_square_coord, 2, 4, 6)

    # Replicate and Position Green Pixels (if they exist)
    if green_pixel_coord is not None:
        # Expanded magenta square top-left coordinates
        exp_top_left_row = magenta_square_coord[0] - 1
        exp_top_left_col = magenta_square_coord[1] - 1

        # Possible offsets (relative to expanded top-left)
        possible_offsets = [
            (0, 1),  # top, 1 right of expanded top-left
            (1, -1), # 1 down, 1 left of expanded top-left
            (1, 1),  # 1 down, 1 right of expanded top-left
            (1, 3),  # 1 down, 3 right of expanded top-left
            (2, 3),  # 2 down, 3 right of expanded top-left
            (4, -1), # 4 down, 1 left of expanded top-left
            (4, 3),  # 4 down, 3 right of expanded top-left
            (5, 1)   # 5 down, 1 right of expanded top left
        ]

        # determine which offsets to use (current best guess - needs improvement)
        used_offsets = []
        input_row, input_col = green_pixel_coord

        # calculate input offset relative to *original* magenta top-left
        input_offset_row = input_row - magenta_square_coord[0]
        input_offset_col = input_col - magenta_square_coord[1]

        # very rough heuristics based on observation
        if input_offset_row < 0 and input_offset_col < 0:  # top left
            used_offsets = [(1,-1), (4, -1)]
        elif input_offset_row < 0: # top
            used_offsets = [(0,1)]
        elif input_offset_col < 0: # left
            used_offsets = [(1,-1), (1, 1), (4, -1)]
        elif input_offset_row >= 2 and input_offset_col >=2:
            used_offsets = [(5,1)]
        elif input_offset_row >=2 and input_offset_col < 2:
            used_offsets = [(4, -1), (4, 3)]
        elif input_offset_row < 2 and input_offset_col > 0:
            used_offsets = [(1,3), (2,3), (4,3)]
        else:
            used_offsets = [(1,1), (1,3)]
        
        for offset in used_offsets:
          new_row = exp_top_left_row + offset[0]
          new_col = exp_top_left_col + offset[1]
          if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
            output_grid[new_row, new_col] = 3
        

    return output_grid