"""
The transformation rule involves moving orange (7) and green (3) objects to a specific row relative to the blue (1) and red (2) objects, and shifting the orange object's column based on the green object's column shift.

1.  **Identify Objects:** Find all contiguous blocks of non-white pixels (objects) in the input grid.  Specifically, pay attention to the orange (7), green (3), blue (1), and red (2) objects.
2.  **Reference Point:** The blue and red pixels always exist, and they are always adjacent, with blue to the left of red.  Consider this pair as an unmoving reference line.
3.  **Determine Output Row:** Orange and green objects are moved to the same row as each other.  The output row is always 3 rows above the blue/red reference.
4.  **Determine Output Columns:** The green object moves to column 10. The orange object moves to column 10 if there is a green object, and to column 9 if there is no green object.

"""

import numpy as np

def find_objects(grid):
    """Finds objects (non-white connected pixels) in the grid."""
    objects = {}
    visited = set()

    def dfs(r, c, color, obj_coords):
        """Depth-first search to find connected components."""
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != 0 and (r, c) not in visited:
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def object_centroid(obj_coords):
    """Calculates the centroid of an object."""
    return np.mean(obj_coords, axis=0)
    
def get_reference_row(input_objects):
    """Gets the row of the blue/red reference line."""
    if 1 in input_objects and 2 in input_objects:
      blue_row = input_objects[1][0][0][0] #just use first coordinate
      return blue_row
    return None


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    #find objects
    input_objects = find_objects(input_grid)
    
    #get reference row
    reference_row = get_reference_row(input_objects)
    target_row = reference_row - 3

    # Handle green (3) object
    if 3 in input_objects:
        for obj_coords in input_objects[3]:
            # Clear current pixels
            for r, c in obj_coords:
                output_grid[r, c] = 0
            
            # Determine new coordinates and set
            for r,c in obj_coords:
                if 0 <= target_row < output_grid.shape[0]:
                  output_grid[target_row,10] = 3

    # Handle orange (7) object
    if 7 in input_objects:
      for obj_coords in input_objects[7]:
          # Clear current pixels
          for r, c in obj_coords:
              output_grid[r, c] = 0

          # Determine new coordinates and set
          for r,c in obj_coords:
              if 0 <= target_row < output_grid.shape[0]:
                if 3 in input_objects:
                  output_grid[target_row,10] = 7
                else:
                  output_grid[target_row,9] = 7
    
    return output_grid