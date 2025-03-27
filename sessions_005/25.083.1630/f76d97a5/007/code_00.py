"""
1.  **Identify "X" Shape:** Examine the input grid and identify if a diagonally connected "X" shape exists.
    *   An "X" shape is formed by a single color.
    *   The "X" must have diagonal contiguity.
    *   The central part of the "X" can be either a single pixel or a 2x2 block of pixels of the same color.

2.  **Preserve "X" Color:** If an "X" shape is found, preserve *only* the pixels of that color in the output grid. All other pixels in the output grid should be set to 0 (background).

3. **Handle "+" Shape:** If no "X" shape exists, then try to identify a "+" shape.
    * A plus is identified by a single color.
    * The center of the "+" shape is a single pixel that is the same color above, below, left, and right.

4. **Preserve "+" Color:** If a "+" shape is found, preserve only the color in the shape.

5. **Update "+" Color:** It seems that the + should use the color present in the corners of the grid

"""

import numpy as np

def find_x_shape(grid):
    """
    Finds the color forming a contiguous 'X' shape in the grid.
    Returns the color if found, otherwise returns None. Considers both 1x1 and 2x2 centers.
    """
    rows, cols = grid.shape
    colors = np.unique(grid)

    for color in colors:
        if color == 0:
            continue

        coords = np.argwhere(grid == color)
        if len(coords) < 5: #minimum for an x
          continue

        # Check for 2x2 center
        center_2x2 = False
        for r in range(rows - 1):
            for c in range(cols - 1):
                if (grid[r, c] == color and grid[r + 1, c] == color and
                    grid[r, c + 1] == color and grid[r + 1, c + 1] == color):
                    center_2x2 = True
                    break
            if center_2x2:
                break

        # check for 1x1 center
        center_1x1 = False
        if not center_2x2:
          for r in range(1,rows - 1):
            for c in range(1, cols - 1):
              if grid[r,c] == color:
                # check diagonals
                if (grid[r-1,c-1] == color or grid[r-1, c+1] == color) and \
                    (grid[r+1, c-1] == color or grid[r+1, c+1] == color):
                  center_1x1 = True
                  break
            if center_1x1: break
          
        if not center_1x1 and not center_2x2: continue

        # Check for contiguity from the center outwards
        min_r, min_c = np.min(coords, axis=0)
        max_r, max_c = np.max(coords, axis=0)
        
        is_x = True
        
        # this part is still very difficult to get right, use the min/max rows
        if center_1x1:

          for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
              # check to see if part of x
              on_diag = False
              
              # check primary diags
              if (r - min_r) == (c - min_c):
                on_diag = True
              
              if center_2x2:
                if (r - min_r) == (c - min_c -1):
                  on_diag = True
                if (r - min_r - 1) == (c - min_c):
                  on_diag = True
              # check cross diag
              if (r-min_r) == (max_c - c):
                on_diag = True
              
              if center_2x2:
                if (r - min_r -1 ) == (max_c - c):
                  on_diag = True
                if (r - min_r) == (max_c - c - 1):
                  on_diag = True
                
              if on_diag and grid[r,c] != color:
                  is_x = False
                  break
              if not on_diag and grid[r,c] == color:
                  is_x = False
                  break
            if not is_x: break

        if is_x:
            return color

    return None

def find_plus_shape(grid):
    """
    Identifies a '+' shape in the grid.
    """
    rows, cols = grid.shape
    colors = np.unique(grid)

    for color in colors:
      if color == 0: continue
      
      for r in range(1, rows - 1):
          for c in range(1, cols - 1):
            if grid[r,c] == color:
              if (grid[r+1, c] == color and grid[r-1, c] == color and grid[r, c+1] == color and grid[r, c-1] == color):
                return color
    return None
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find X shape color
    x_color = find_x_shape(input_grid)

    if x_color is not None:
        # Preserve X shape color
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if input_grid[r, c] == x_color:
                    output_grid[r, c] = x_color
    else:
      #look for plus
      plus_color = find_plus_shape(input_grid)
      
      if plus_color is not None:
        # use color from upper left
        plus_new_color = input_grid[0,0]
        for r in range(input_grid.shape[0]):
          for c in range(input_grid.shape[1]):
            if input_grid[r, c] == plus_color:
              output_grid[r,c] = plus_new_color

    return output_grid