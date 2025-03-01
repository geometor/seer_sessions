"""
1.  **Identify Objects:** Find all contiguous blocks of pixels with the same color.
2. **Move Objects in Top Row**: Objects with any part of them in the top row (row 0) will move down by one row.
3. **Preserve Other Objects**: All other objects that are not in the top row will remain in their original position.
4.  **Background:** The background is color 0 (white). Fill any vacated cells with the background color.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous blocks of the same color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, object_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        object_coords.append((r, c))
        dfs(r + 1, c, color, object_coords)
        dfs(r - 1, c, color, object_coords)
        dfs(r, c + 1, color, object_coords)
        dfs(r, c - 1, color, object_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                object_coords = []
                dfs(r, c, grid[r, c], object_coords)
                objects.append({
                    'color': grid[r, c],
                    'coords': object_coords
                })
    return objects

def is_top_row(object_coords):
    """Checks if an object is in the top row."""
    for r, _ in object_coords:
        if r == 0:
            return True
    return False

def move_object_down(object_coords, grid_height):
    """Moves object coordinates down by one row if possible."""
    new_coords = []
    for r, c in object_coords:
        if r + 1 < grid_height:
          new_coords.append((r + 1, c))
        else:
          return None # can't move down
    return new_coords

def transform(input_grid):
    # initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid)

    # Find all objects in the grid
    objects = find_objects(input_grid)

    # Process each object
    for obj in objects:
        # Check if the object is in the top row
        if is_top_row(obj['coords']):
            # Move the object down by one row
            new_coords = move_object_down(obj['coords'], input_grid.shape[0])
            if new_coords != None:
              for r, c in new_coords:
                  output_grid[r, c] = obj['color']
            else:
              for r,c in obj['coords']:
                output_grid[r,c] = obj['color']
        else:
            # Keep the object in its original position
            for r, c in obj['coords']:
                output_grid[r, c] = obj['color']

    return output_grid