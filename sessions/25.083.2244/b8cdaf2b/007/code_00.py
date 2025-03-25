"""
1.  **Identify Objects:**
    *   Object 1: The lowest row of the input grid containing non-zero values.
    *   Object 2: The contiguous block of pixels *above* Object 1, connected to
        object 1, that is a different color than any color in object 1.

2.  **Find the edge colors**:
    * The left-most and right-most colors of object one.

3.  **Propagate Edge Colors:**
    * For each pixel along the edges of the grid containing the edge colors,
      propagate this color vertically upwards into Object 2, replacing any
      connected pixels of the same color *until* a different color or an empty
      cell is encountered.

4.  **Fill Between Edges**:
    * Find the Object 2 pixels between the two propagated edge colors. Replace
      these pixels by alternating the colors present at the border between the
      bottom-most row of object 2 and object 1. Start with the color from the left.

5.  **Preserve Other Pixels:** All other pixels in the grid retain their original values.

6.  **Output:** Return the modified grid.
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
        connected_object2 = []
        
        def is_connected(coord):
          r,c = coord
          if (r+1, c) in object1_coords:
            return True
          neighbors = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
          for nr, nc in neighbors:
              if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                  if (nr,nc) in object2_coords:
                    return True
          return False
        
        for r,c in object2_coords:
            if is_connected((r,c)):
                connected_object2.append((r,c))
        object2_coords = connected_object2

    return object1_coords, object2_coords

def get_edge_colors(grid, object1_coords):
    if not object1_coords:
        return None, None
    
    # Sort by column index to find leftmost and rightmost
    sorted_coords = sorted(object1_coords, key=lambda x: x[1])
    leftmost_color = grid[sorted_coords[0]]
    rightmost_color = grid[sorted_coords[-1]]
    return leftmost_color, rightmost_color

def propagate_edge_colors(grid, object1_coords, object2_coords):
    
    leftmost_color, rightmost_color = get_edge_colors(grid, object1_coords)
    
    if leftmost_color is not None:
      #find leftmost edge column:
      left_col = [c for r,c in object1_coords if grid[r,c] == leftmost_color][0]

      #propagate up
      for r in range(object1_coords[0][0] -1, -1, -1):
          if grid[r, left_col] != 0:
            grid[r, left_col] = leftmost_color
          else:
            break
    
    if rightmost_color is not None:
      #find leftmost edge column:
      right_col = [c for r,c in object1_coords if grid[r,c] == rightmost_color][-1]
      #propagate up
      for r in range(object1_coords[0][0] -1, -1, -1):
        if grid[r, right_col] != 0:
            grid[r, right_col] = rightmost_color
        else:
            break
      
    return grid

def fill_between_edges(grid, object1_coords, object2_coords):
    if not object1_coords or not object2_coords:
      return grid
    
    leftmost_color, rightmost_color = get_edge_colors(grid, object1_coords)
    left_col = min(c for r, c in object1_coords)
    right_col = max(c for r, c in object1_coords)

    object1_row = object1_coords[0][0]
    
    
    for r in range(object1_row - 1, -1, -1):  # Iterate upwards from object1
      alternate = True
      for c in range(left_col + 1, right_col):
          if (r,c) in object2_coords or grid[r,c] != 0:
              if alternate:
                  grid[r, c] = leftmost_color
              else:
                  grid[r, c] = rightmost_color
              alternate = not alternate


    return grid


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    input_grid_np = np.array(input_grid)

    # Find objects
    object1_coords, object2_coords = find_objects(input_grid_np)

    #get edge colors
    output_grid = propagate_edge_colors(output_grid, object1_coords, object2_coords)

    # fill between edges
    output_grid = fill_between_edges(output_grid, object1_coords, object2_coords)

    return output_grid.tolist()