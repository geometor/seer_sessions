"""
The transformation rule identifies 'cross' shaped objects in the input grid and expands them into solid squares of the same color in the output grid. The expanded square is then shifted based on the original position of the cross.
"""

import numpy as np

def find_cross_center(grid):
    """Finds the center of cross-shaped objects in the grid."""
    centers = []
    rows, cols = grid.shape

    def is_cross_like(r, c, color):

        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if grid[r,c] != color:
            return False

        # check counts of rows and cols
        row_counts = {}
        col_counts = {}

        pixels = []
        visited = set()
        def dfs(row, col):
          nonlocal row_counts, col_counts, pixels
          if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
          visited.add((row,col))
          pixels.append((row,col))
          row_counts[row] = row_counts.get(row,0) + 1
          col_counts[col] = col_counts.get(col,0) + 1
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc)

        dfs(r,c)
        
        # modification: allow more than 5
        if len(pixels) < 5:
          return False
        
        if len(row_counts) >= 3 and len(col_counts) >= 3:
           # check for center
           has_center = False
           for row in row_counts:
               for col in col_counts:
                   if (row,col) in pixels:
                       # count neighbors:
                       neighbor_count = 0
                       for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                           nrow, ncol = row + dr, col + dc
                           if 0 <= nrow < rows and 0 <= ncol < cols and (nrow, ncol) in pixels:
                               neighbor_count+=1
                       if neighbor_count >=3:
                          has_center = True
                          break
               if has_center:
                 break

           return has_center
        return False

    for r in range(rows):
        for c in range(cols):
            if is_cross_like(r, c, grid[r,c]):
                
                pixels = []
                visited = set()
                def dfs(row, col,color):
                    if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
                        return
                    visited.add((row,col))
                    pixels.append((row,col))

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        dfs(row + dr, col + dc, color)
                dfs(r,c,grid[r,c])

                rows, cols = zip(*pixels)
                centers.append( ( int(round(np.mean(rows))), int(round(np.mean(cols))))    )

    return centers

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append(obj)
    return objects

def is_cross_shaped(grid, object_pixels):
    """
    Checks if an object has a 'cross' shape.
    """
    if len(object_pixels) < 5: # optimization: a cross needs at least 5 pixels
      return False

    rows, cols = zip(*object_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # check counts of rows and cols
    row_counts = {}
    col_counts = {}

    for r,c in object_pixels:
      row_counts[r] = row_counts.get(r,0) + 1
      col_counts[c] = col_counts.get(c,0) + 1
      
    if len(row_counts) >= 3 and len(col_counts) >= 3:
        # check for center
        has_center = False
        for row in row_counts:
            for col in col_counts:
                if (row,col) in object_pixels:
                    # count neighbors:
                    neighbor_count = 0
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nrow, ncol = row + dr, col + dc
                        if 0 <= nrow < len(grid) and 0 <= ncol < len(grid[0]) and (nrow, ncol) in object_pixels:
                            neighbor_count+=1
                    if neighbor_count >=3:
                        has_center = True
                        break
            if has_center:
                break

        return has_center
  
    return False


def expand_to_square(object_pixels):
    """
    Expands the object to its bounding square.
    """
    rows, cols = zip(*object_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    square_pixels = []
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            square_pixels.append((r, c))
    return square_pixels

def calculate_shift(input_grid, cross_center):
    """Calculates target center based on an alignment strategy."""
    rows, cols = input_grid.shape
    r, c = cross_center

    # find closest non-zero edge in input
    #   if no non-zero edge exists, use grid edge
    
    # for now, return cross_center - but eventually we need to calculate a shift

    return cross_center

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find objects
    objects = find_objects(input_grid)
    
    # Process each object
    for obj in objects:
        color = input_grid[obj[0]]
        if is_cross_shaped(input_grid, obj):
            # Expand to square if cross-shaped
            square = expand_to_square(obj)
            # find the center of cross
            cross_center = find_cross_center(input_grid)
            if len(cross_center) > 0: # there should only ever be 1
              target_center = calculate_shift(input_grid, cross_center[0])


              # shift the expanded object
              row_shift = target_center[0] - cross_center[0]
              col_shift = target_center[1] - cross_center[1]

              for r, c in square:
                  shifted_r, shifted_c = r + row_shift, c + col_shift
                  if 0 <= shifted_r < output_grid.shape[0] and 0 <= shifted_c < output_grid.shape[1]:
                    output_grid[shifted_r, shifted_c] = color
        # else skip - no other objects need to be transformed

    return output_grid