"""
1.  **Identify Green Shapes:** Locate all contiguous regions of green (3) pixels. These form the "green shapes."

2.  **Identify Red Pixels:** Locate all red (2) pixels that either inside a green object or adjacent to the green shapes.

3.  **Extend Red Vertically:** For each identified red pixel, copy and extend the red color, but limited within the green shape, in the following way:
      * If the red pixel is inside the green object, then we copy the entire column of green to red
      * If the red pixel is outside the green object, then we copy the red color until a 2-pixel vertical segment of color 3 is encountered. If the current red color is in a column, we need to copy and extend the color horizontally, until a 2-pixel horizontal segment of color 3.

4. The background pixels remains the same.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of a specific color."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_adjacent(pixel, green_shape):
    """Checks if a pixel is adjacent to a green shape."""
    r, c = pixel
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if (nr, nc) in green_shape:
            return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find green objects
    green_objects = find_objects(input_grid, 3)
    
    # flatten list of green objects to one list of green pixels
    green_pixels = []
    for obj in green_objects:
        green_pixels.extend(obj)


    # find red pixels
    red_pixels = [(r, c) for r in range(rows) for c in range(cols) if input_grid[r, c] == 2]

    # extend red according to the rules.
    for r, c in red_pixels:
      if (r,c) in green_pixels:
        # find the green object the pixel belongs to
        current_green_object = None
        for obj in green_objects:
          if (r,c) in obj:
            current_green_object = obj
            break
        # convert entire object to red
        if current_green_object is not None:
            for gr, gc in current_green_object:
                output_grid[gr,gc] = 2
      else:
        # check whether pixel is adjacent
        is_adj = False
        for obj in green_objects:
          if is_adjacent((r,c), obj):
              is_adj = True
              current_green_object = obj
              break
        
        if is_adj:
          # we extend vertically
            for gr, gc in current_green_object:
              if gc == c:
                output_grid[gr, gc] = 2

    return output_grid