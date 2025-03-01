# b775ac94 • 014 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all distinct colored objects in the input grid. An object is a contiguous block of pixels of the same color.
2.  **Scale Each Object:** For each object found, create a scaled-up version.  The scaled version replaces each pixel in the original object with a 2x2 block of pixels of the same color. The relative positions of the pixels within the object are maintained.
3.  **Reflect Each Scaled Object**: Create a reflected version of each scaled object. The reflection is across a horizontal axis. The reflected object is positioned directly below the scaled object. The top edge of the reflected object will start on the row immediately after the last row occupied by the scaled object. The x coordinates (columns) will be the same as corresponding pixels in the scaled object.
4. **Combine and Output**: Create output grid large enough for the combined scaled and reflected objects. Place each object and its reflected object in to the output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    Returns a dictionary of objects, where each object is represented by a list of its pixel coordinates.
    """
    objects = {}
    visited = set()

    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                neighbors.append((nr, nc))
        return neighbors

    def dfs(r, c, color, obj_id):
        visited.add((r, c))
        objects[obj_id].append((r, c))

        for nr, nc in get_neighbors(r, c):
            if (nr, nc) not in visited and grid[nr, nc] == color:
                dfs(nr, nc, color, obj_id)

    obj_id_counter = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                objects[obj_id_counter] = []
                dfs(r, c, grid[r, c], obj_id_counter)
                obj_id_counter += 1
    return objects

def scale_object(pixels):
    """Scales a single object to a 2x2 square for each pixel."""
    scaled_pixels = []
    for r, c in pixels:
        scaled_pixels.extend([(r * 2, c * 2), (r * 2, c * 2 + 1), (r * 2 + 1, c * 2), (r * 2 + 1, c * 2 + 1)])
    return scaled_pixels

def reflect_object(scaled_pixels):
    """Reflects a scaled object vertically."""
    max_row = max(r for r, _ in scaled_pixels)
    reflected_pixels = []
    for r, c in scaled_pixels:
        reflected_pixels.append((2 * max_row - r + 2 , c)) #+2 because of the scaling
    return reflected_pixels
    

def transform(input_grid):
    """
    Transforms the input grid according to the defined rule.
    """
    input_grid = np.array(input_grid)

    # 1. Identify Objects
    objects = find_objects(input_grid)

    # 2. & 3. Scale and Reflect each object
    scaled_objects = {}
    reflected_objects = {}

    for obj_id, pixels in objects.items():
        scaled_objects[obj_id] = scale_object(pixels)
        reflected_objects[obj_id] = reflect_object(scaled_objects[obj_id])
    
    # find boundary to create output grid
    max_r = 0
    max_c = 0

    # Combine scaled and reflected objects for boundary calculation
    for obj_id in objects:
      for r,c in scaled_objects[obj_id]:
         max_r = max(r, max_r)
         max_c = max(c, max_c)
      for r,c in reflected_objects[obj_id]:
         max_r = max(r, max_r)
         max_c = max(c, max_c)
    output_grid = np.zeros((max_r + 1, max_c + 1), dtype=int)
    
    # Place the objects
    for obj_id in objects:
      color = input_grid[objects[obj_id][0][0], objects[obj_id][0][1]]  # Get color of object

      # fill the scaled object
      for r, c in scaled_objects[obj_id]:
          output_grid[r,c] = color

      # fill the reflected object
      for r,c in reflected_objects[obj_id]:
          output_grid[r,c] = color

    return output_grid.tolist()
```
