"""
The transformation identifies gray (5) objects in the input grid and fills
internal and adjacent "empty" (white, 0) spaces with azure (8) based on the
shape and location of the gray objects. It also has a specific rule for filling
a row above horizontal gray objects in some cases.
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

def is_adjacent(grid, r, c, object_pixels):
    """
    Checks if a given white (0) cell is adjacent a gray object.
    'Adjacent' a cell that has gray as a neighbour, including diagonals.
    """

    rows, cols = grid.shape

    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))

    # neighbour must be gray or part of object.
    for nr, nc in neighbors:
      if (nr, nc) in object_pixels or grid[nr,nc] == 5:
            return True
    return False

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Gray Objects
    gray_objects = get_objects(input_grid, 5)

    # Iterate through each gray object
    for obj_pixels in gray_objects:
        # 2. Fill Internal Spaces & 3. Fill Adjacent Cells
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] == 0:  # If white pixel
                  if is_inside(input_grid, r, c, obj_pixels):
                    output_grid[r, c] = 8 #fill azure
                  elif is_adjacent(input_grid,r,c,obj_pixels):
                    output_grid[r,c] = 8
    
    # 4. Fill Row Above (Example 2 Specific)
    for obj_pixels in gray_objects:
        # Find the top row of the object and its horizontal extent
        min_row = min(r for r, _ in obj_pixels)
        if min_row > 0:  # Ensure there's a row above
            min_col = min(c for _, c in obj_pixels)
            max_col = max(c for _, c in obj_pixels)
            
            # Check all cells for this object
            is_horizontal = True
            for r,c in obj_pixels:
              if not (min_col <= c <= max_col):
                is_horizontal = False
                break

            if is_horizontal:
                for c in range(min_col, max_col + 1):
                    if output_grid[min_row - 1, c] == 0:
                        output_grid[min_row - 1, c] = 8


    return output_grid