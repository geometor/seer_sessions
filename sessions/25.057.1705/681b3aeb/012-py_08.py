"""
1.  **Object Identification:** Identify all contiguous regions of non-white pixels in the input grid. These regions represent objects. Note the color of each object.
2.  **Output Grid Initialization:** Create a 3x3 output grid initialized with all zeros (white).
3.  **Magenta Placement:** Fill the top row and the rightmost column of the output grid with magenta (6).
4.  **Find Magenta Width:** Find the width of the magenta pixels.
5.  **Yellow Placement:** If there are any yellow objects in the input: Create a yellow (4) vertical line of height equal to the magenta width, up to a maximum height of 2 (the remaining rows), starting at output position (1,0).
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = {}
    visited = set()

    def dfs(r, c, color, obj_id):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return []
        visited.add((r, c))
        coords = [(r, c)]
        coords.extend(dfs(r + 1, c, color, obj_id))
        coords.extend(dfs(r - 1, c, color, obj_id))
        coords.extend(dfs(r, c + 1, color, obj_id))
        coords.extend(dfs(r, c - 1, color, obj_id))
        return coords

    obj_counter = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_id = obj_counter
                obj_counter +=1
                objects[obj_id] = {
                    'color': grid[r, c],
                    'coords': dfs(r, c, grid[r, c], obj_id)
                }
    return objects

def get_magenta_width(input_grid, objects):
    """Calculates the width of the magenta object."""
    magenta_coords = []
    for obj_id, obj_data in objects.items():
        if obj_data['color'] == 6:
            magenta_coords.extend(obj_data['coords'])

    if not magenta_coords:
        return 0

    magenta_coords = np.array(magenta_coords)
    min_col = np.min(magenta_coords[:, 1])
    max_col = np.max(magenta_coords[:, 1])
    return max_col - min_col + 1


def transform(input_grid):
    # Object Identification
    objects = find_objects(input_grid)

    # Output Grid Initialization
    output_grid = np.zeros((3, 3), dtype=int)

    # Magenta Placement
    output_grid[0, :] = 6  # Top row
    output_grid[:, 2] = 6  # Rightmost column

    # Find Magenta width
    magenta_width = get_magenta_width(input_grid, objects)
    
    # Yellow Placement
    yellow_exists = any(obj_data['color'] == 4 for obj_data in objects.values())
    if yellow_exists:
      height = min(2, magenta_width)
      for i in range(height):
        output_grid[i+1,0]=4


    return output_grid