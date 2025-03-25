"""
The transformation identifies gray (5) objects in the input grid and fills
internal and adjacent "empty" (white, 0) spaces with azure (8) based on the
shape and location of the gray objects. It fills the space between adjacent
horizontal gray lines. It has a specific rule for filling a single row segment
above horizontal gray objects in some cases, only directly above and only for
the top edge of the object.
"""

import numpy as np

def get_objects(grid, color):
    """
    Finds contiguous objects of a specific color in the grid.
    Returns a list of lists, where each inner list contains the (row, col)
    coordinates of pixels belonging to an object.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(r, c, current_object):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                dfs(r + i, c + j, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_inside(grid, r, c, object_pixels):
    """
    Checks if a given white (0) cell is inside a gray object.
    'Inside' means fully enclosed by gray pixels, including diagonals.
    """

    rows, cols = grid.shape
    
    # Quick check for edge cases to avoid unnecessary checks
    if r <= 0 or r >= rows - 1 or c <= 0 or c >= cols - 1:
      return False

    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nr, nc = r + i, c + j
            neighbors.append((nr, nc))

    # All neighbors must be gray or part of object.
    for nr, nc in neighbors:
      if (nr, nc) not in object_pixels and grid[nr,nc] != 5:
            return False
    return True

def fill_between_horizontal_lines(grid, output_grid, gray_objects):
    """
    Fills the space between adjacent horizontal gray lines with azure (8).
    """
    if len(gray_objects) < 2:
      return

    rows, cols = grid.shape
    # Check if there's more than one row of gray objects
    row_set = set()
    for obj in gray_objects:
        for r, _ in obj:
          row_set.add(r)
    
    if len(row_set) > 1 :

      # Create set of all gray pixels
      gray_pixels = set()
      for obj_pixels in gray_objects:
        gray_pixels.update(obj_pixels)

      # Find all horizontal lines by looking at gray pixel sets
      h_lines = {}
      for r, c in gray_pixels:
          if r not in h_lines:
            h_lines[r] = []
          h_lines[r].append(c)
      
      sorted_rows = sorted(h_lines.keys())
      
      # Fill between adjacent horizontal gray lines
      for i in range(len(sorted_rows) - 1):
          r1 = sorted_rows[i]
          r2 = sorted_rows[i+1]
          
          # only fill between adjacent lines
          if r2 - r1 == 1:
            continue
          
          # find overlapping columns and fill in between
          cols1 = set(h_lines[r1])
          cols2 = set(h_lines[r2])
          overlap_cols = sorted(list(cols1.intersection(cols2)))

          if overlap_cols:
              for c in overlap_cols:
                  for r in range(r1 + 1, r2):
                      if output_grid[r,c] == 0:
                        output_grid[r, c] = 8

def fill_above_top_edge(grid, output_grid, gray_objects):
    """
    Fills one row above the topmost horizontal edge of gray objects.
    """
    # Find the *top* row among all objects
    min_row = grid.shape[0]  # Initialize with a large value
    for obj_pixels in gray_objects:
        min_row = min(min_row, min(r for r, _ in obj_pixels))

    if min_row > 0:
        # Collect all top edge pixels from all gray objects
        top_edge_pixels = []
        for obj_pixels in gray_objects:
          for r,c in obj_pixels:
            if r == min_row:
              top_edge_pixels.append((r,c))

        # Fill the row above
        for r, c in top_edge_pixels:
            if output_grid[min_row - 1, c] == 0:
                output_grid[min_row - 1, c] = 8

def fill_adjacent(grid, output_grid, gray_objects):

    rows, cols = grid.shape
    
    for obj_pixels in gray_objects:
      for r, c in obj_pixels: #Iterate object pixels
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 0:
                    output_grid[nr, nc] = 8
    

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Gray Objects
    gray_objects = get_objects(input_grid, 5)

    # 2. Fill Internal Cavities
    for obj_pixels in gray_objects:
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] == 0:  # If white pixel
                  if is_inside(input_grid, r, c, obj_pixels):
                    output_grid[r, c] = 8 #fill azure
    
    # 3. Fill Specific Adjacency, part 1: Fill adjacent white cells between two horizontal gray lines
    fill_between_horizontal_lines(input_grid, output_grid, gray_objects)

    # 4. Fill Above Top Horizontal Edge
    fill_above_top_edge(input_grid, output_grid, gray_objects)

    # 5. Fill Specific Adjacency, part 2: Fill adjacent cells to gray cells
    fill_adjacent(input_grid, output_grid, gray_objects)
    
    return output_grid