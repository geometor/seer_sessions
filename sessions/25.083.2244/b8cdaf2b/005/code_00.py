"""
1.  **Identify Objects:**
    *   Object 1: The lowest row of the input grid containing non-zero values.
    *   Object 2: The contiguous block of pixels *above* Object 1, that contains at least one pixel of a different color than any colors in object 1.

2.  **Select Source Pixels:**
    *   Iterate through each pixel in Object 2.
    *   For each pixel in Object 2, check if there is a pixel directly *below* it (in Object 1).
    *   If a pixel exists directly below, and that lower pixel has any color from the set of object 1 colors, then: the position of the object 2 pixel is where object 1's color should be copied.

3.  **Copy and Shift:** For each of the located Object 2 pixels, replace with the color of the Object 1 pixel directly below.

4.  **Preserve Other Pixels:** All other pixels in the grid retain their original values.

5.  **Output:** Return the modified grid.
"""

import numpy as np

def find_objects(grid):
    # Find the lowest row with non-zero values
    non_zero_rows = np.where(np.any(grid != 0, axis=1))[0]
    if not non_zero_rows.size:
        return [], []

    last_row_index = non_zero_rows[-1]
    last_row = grid[last_row_index]
    object1_coords = [(last_row_index, c) for c, value in enumerate(last_row) if value != 0]
    if not object1_coords:
        return [],[]
    object1_colors = set([grid[r,c] for r,c in object1_coords])

    object2_coords = []
    for r in range(last_row_index):
        for c in range(grid.shape[1]):
          if grid[r,c] != 0 and grid[r,c] not in object1_colors:
            object2_coords.append((r,c))
    
    #remove object 2 coordinates not connected
    if len(object2_coords) > 0:
        object2_color = grid[object2_coords[0]]
        connected_object2 = []
        
        def is_connected(coord, color):
          r,c = coord
          neighbors = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
          for nr, nc in neighbors:
              if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                  if (nr,nc) in object2_coords and grid[nr,nc] == color:
                    return True
          return False
        
        for r,c in object2_coords:
            if grid[r,c] == object2_color and is_connected((r,c), object2_color):
                connected_object2.append((r,c))
        object2_coords = connected_object2

    return object1_coords, object2_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    input_grid_np = np.array(input_grid)

    # Find objects
    object1_coords, object2_coords = find_objects(input_grid_np)
    object1_colors = set([input_grid_np[r,c] for r,c in object1_coords])

    # Iterate through object 2 pixels
    for r2, c2 in object2_coords:
      #check for object 1 pixel below
      if (r2+1,c2) in object1_coords:
        output_grid[r2,c2] = input_grid_np[r2+1,c2]

    return output_grid.tolist()