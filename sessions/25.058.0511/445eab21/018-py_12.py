"""
1.  **Identify Yellow Squares:** Examine the input grid and locate all objects that are squares and colored yellow. These squares can be either hollow or filled.
2. **Conditional Extraction:**
   * If one or more *hollow* yellow squares are found, extract the 2x2 subgrid at the top-left corner of the *smallest* such hollow square.
   * If *no hollow* yellow squares are found but a *filled* yellow square filling the entire grid exists, extract the 2x2 subgrid at the top-left corner of the entire grid.
3. **Output:** Return the extracted 2x2 subgrid.
"""

import numpy as np

def get_objects(grid):
    """
    Find contiguous regions of the same color and return them as a list of objects.
    Each object is a dictionary containing the color, and the set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj_coords):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_coords.add((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                if color != 0:
                  obj_coords = set()
                  dfs(row, col, color, obj_coords)
                  objects.append({"color": color, "coords": obj_coords})
    return objects

def is_hollow_square(coords, grid):
    """
    Checks if a set of coordinates forms a hollow square.
    """
    if not coords:
        return False

    rows, cols = zip(*coords)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Check if it's a square
    if (max_row - min_row) != (max_col - min_col):
        return False

    # Check if it's hollow
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if (r > min_row and r < max_row) and (c > min_col and c < max_col):
                if (r, c) in coords:
                    return False  # Inner part should be empty
            else:
                if (r, c) not in coords:
                    return False # Border should be complete
    return True

def is_filled_square(coords, grid):
    """
    Checks if a set of coordinates forms a filled square.
    """
    if not coords:
        return False

    rows, cols = zip(*coords)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Check if it's a square
    if (max_row - min_row) != (max_col - min_col):
        return False
    for r in range(min_row, max_row+1):
        for c in range(min_col, max_col+1):
            if (r,c) not in coords:
                return False
    return True

def get_square_size(coords):
    """Calculates the size of a square given its coordinates."""
    rows, cols = zip(*coords)
    return max(rows) - min(rows) + 1


def transform(input_grid):
    # Find objects
    objects = get_objects(input_grid)

    # Find yellow squares
    yellow_squares = []
    for obj in objects:
        if obj['color'] == 4:
          if is_hollow_square(obj['coords'], input_grid) or is_filled_square(obj['coords'],input_grid):
            yellow_squares.append(obj)

    # initialize with background
    output_grid = np.zeros((2, 2), dtype=int)

    # Conditional Extraction
    if yellow_squares:
      hollow_yellow_squares = [obj for obj in yellow_squares if is_hollow_square(obj['coords'], input_grid)]

      if hollow_yellow_squares:
        # find smallest
        smallest_hollow_square = min(hollow_yellow_squares, key=lambda x: get_square_size(x['coords']))

        # Get the top-left corner coordinates of the smallest hollow square
        min_row = min(coord[0] for coord in smallest_hollow_square['coords'])
        min_col = min(coord[1] for coord in smallest_hollow_square['coords'])

      elif is_filled_square(yellow_squares[0]['coords'], input_grid) and get_square_size(yellow_squares[0]['coords']) == input_grid.shape[0]:
          min_row, min_col = 0,0 # it's full grid
      else:
          return output_grid # should not get here based on the natural language program

      # copy the 2x2 region
      for r in range(2):
        for c in range(2):
          if min_row + r < input_grid.shape[0] and min_col + c < input_grid.shape[1]:
            output_grid[r, c] = input_grid[min_row + r, min_col + c]
    return output_grid