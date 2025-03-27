"""
1.  **Identify Objects:** Divide the input grid into two objects.
    *   Object 1 is composed of the lowest row containing non-zero values.
    *   Object 2 is the contiguous block *above* Object 1 with a different color.

2.  **Select Source Pixels:** Within Object 1, select only those pixels that have a pixel of Object 2's color directly above them.

3.  **Copy and Shift:** Copy the color of the selected pixels from Object 1 to the grid cell directly above them (one row up).

4.  **Preserve Other Pixels:** All other pixels in the grid retain their original values.

5.  **Output:** Generate the output grid.
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
    object1_color = grid[object1_coords[0]] #color of the first pixel

    object2_coords = []
    for r in range(last_row_index):
        for c in range(grid.shape[1]):
          if grid[r,c] != 0 and grid[r,c] != object1_color:
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

def select_source_pixels(grid, object1_coords, object2_coords):
    
    if not object2_coords:
      return []
      
    object2_color = grid[object2_coords[0]]
    source_pixels = []
    for r1, c1 in object1_coords:
        for r2, c2 in object2_coords:
            if r1 - 1 == r2 and c1 == c2 and grid[r2,c2] == object2_color:
                source_pixels.append((r1, c1))
                break  # Ensure only one match per object1 pixel
    return source_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    input_grid_np = np.array(input_grid)


    # Find objects
    object1_coords, object2_coords = find_objects(input_grid_np)

    # Select source pixels
    source_pixels = select_source_pixels(input_grid_np, object1_coords, object2_coords)

    # Copy and shift
    for r, c in source_pixels:
        if r > 0:
            output_grid[r - 1, c] = input_grid_np[r, c]

    return output_grid.tolist()