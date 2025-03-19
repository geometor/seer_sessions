"""
1.  **Identify Plus Shapes:** Scan the input grid to locate all "plus-shaped" objects. A plus-shaped object is defined as a contiguous set of orange (7) pixels forming a '+' shape, with a single red (2) pixel at its geometric center. The center must have exactly 4 orange pixels as neighbors.
2.  **Expand Plus Shapes:** For each identified plus shape, expand it outwards by one pixel in all four cardinal directions (up, down, left, right) creating a hollow rectangle. The outline of this expanded shape consists of orange (7) pixels. The original red (2) pixel at the center of the plus shape should remain unchanged. This creates the smallest rectangle that encompasses the plus shape.
3.  **Fill Between Expanded Shapes:** Fill the area *between* the orange edges of the expanded shapes with red (2) pixels.  This fill should extend up to, but not overwrite, the orange (7) pixels forming the borders of the expanded shapes. The fill operation does *not* fill the entire image or any area not enclosed by orange borders. The original red center pixels are *not* filled over.
"""

import numpy as np

def find_plus_objects(grid):
    """Finds plus-shaped objects (7s surrounding a 2)."""
    objects = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] not in (2, 7):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, obj)
        dfs(r - 1, c, obj)
        dfs(r, c + 1, c)
        dfs(r, c - 1, c)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7 and not visited[r, c]:
                obj = []
                dfs(r, c, obj)
                # Check if it's a plus shape with a 2 in the center
                if any(grid[row, col] == 2 for row, col in obj):
                   is_plus = True
                   center = None
                   for row,col in obj:
                       if grid[row,col] == 2:
                           if center is not None:
                               is_plus = False
                               break # only 1 center of 2 allowed
                           else:
                               center = (row,col)
                   if is_plus:
                        orange_neighbors = 0
                        if center:
                            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                nr, nc = center[0] + dr, center[1] + dc
                                if is_valid(nr,nc) and grid[nr,nc] == 7:
                                     orange_neighbors += 1
                        if orange_neighbors == 4:
                            objects.append(obj)
    return objects

def get_bounding_box(plus_object):
    """Calculates the bounding box for a plus object."""
    min_r, min_c = plus_object[0]
    max_r, max_c = plus_object[0]
    for r, c in plus_object:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def expand_plus(grid, plus_object):
    """Expands the plus object to its bounding box and colors it orange."""
    min_r, min_c, max_r, max_c = get_bounding_box(plus_object)
    expanded_object = []

    for r in range(min_r - 1, max_r + 2):
        for c in range(min_c - 1, max_c + 2):
             expanded_object.append((r,c))
    return expanded_object


def fill_between_objects(grid, expanded_objects):
    """Fills the area between expanded objects with red (2)"""
    rows, cols = grid.shape
    
    # Create a set of all expanded object coordinates
    all_expanded_coords = set()
    for obj in expanded_objects:
        for r, c in obj:
            all_expanded_coords.add((r,c))
            
    min_r, min_c, max_r, max_c = rows, cols, 0, 0

    #get combined bounding box of all expanded objects
    for r,c in all_expanded_coords:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
            
    # Flood fill algorithm starting from each edge, stopping at orange pixels
    visited = np.zeros((rows, cols), dtype=bool)
    
    def is_valid(r,c):
        return 0 <= r < rows and 0 <= c < cols
    
    def fill(r,c):
      if not is_valid(r,c) or visited[r,c] or grid[r,c] == 7 or (r,c) in all_expanded_coords:
        return
    
      visited[r,c] = True
      grid[r,c] = 2
      
      fill(r+1,c)
      fill(r-1,c)
      fill(r,c+1)
      fill(r,c-1)
      

    #top edge
    for c in range(cols):
        if is_valid(0, c):
           fill(0, c)
           
    #bottom edge
    for c in range(cols):
       if is_valid(rows-1, c):
          fill(rows-1, c)
    
    #left edge
    for r in range(rows):
      if is_valid(r, 0):
        fill(r, 0)
        
    #right edge
    for r in range(rows):
      if is_valid(r, cols-1):
        fill(r, cols - 1)
        
    #fill internal areas
    for r in range(rows):
      for c in range(cols):
          if is_valid(r,c) and not visited[r,c] and (r,c) not in all_expanded_coords:
              if grid[r,c] != 7:
                  grid[r,c] = 2


def transform(input_grid):
  """Transforms the input grid based on the plus shape expansion and fill rule."""
  grid = np.array(input_grid)
  output_grid = np.copy(grid)

  # 1. Find plus-shaped objects
  plus_objects = find_plus_objects(grid)

  # 2. Expand the plus-shapes
  expanded_objects = []
  for obj in plus_objects:
      expanded = expand_plus(grid, obj)
      expanded_objects.append(expanded)
      for r, c in expanded:
          if output_grid[r, c] != 2: # keep the original red center
            output_grid[r, c] = 7
          

  # 3. Fill between expanded objects
  if expanded_objects:
      fill_between_objects(output_grid, expanded_objects)
  return output_grid