# 3de23699 • 014 • refine_coder

---
```python
"""
1. Identify Green Objects: Find all contiguous blocks of green pixels (green objects) in the input grid.
2. Check Touching Condition: For each green object, determine if it is touching any pixel that is not white (0) and not green (3). "Touching" means adjacent horizontally or vertically (not diagonally).
3. Create Output Grid: Create a new, initially empty, output grid.
4. Stack and Position: For each green object that satisfies the condition, copy it to the output grid. Stack these objects vertically, starting from the top-left corner (0,0) of the output grid. Preserve the shape of each green object. If multiple object are present, order the placement from top-to-bottom, then left-to-right based on the original input position.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous objects of the specified color in the grid.
    Returns a list of objects, where each object is a list of (row, col) tuples.
    """
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_touching(object_pixels, grid, excluded_colors):
    """
    Checks if an object (list of pixels) is touching any pixel of the excluded colors.
    """
    rows, cols = grid.shape
    for r, c in object_pixels:
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] in excluded_colors:
                return True
    return False

def transform(input_grid):
    # Convert to numpy array
    grid = np.array(input_grid)

    # 1. Identify Green Objects
    green_objects = find_objects(grid, 3)

    # 2. Check Touching Condition
    filtered_objects = []
    excluded_colors = {0, 3} # Colors to exclude for touching check, white and green
    all_colors = set(range(10))
    touching_colors = all_colors - excluded_colors

    for obj in green_objects:
        if is_touching(obj, grid, touching_colors):
            filtered_objects.append(obj)

    # 3. Create Output Grid (initialize with zeros)
    # Determine output grid size based on filtered objects.  Could be empty.
    if not filtered_objects:
        return []
    
    max_height = 0
    for obj in filtered_objects:
      min_r = min(p[0] for p in obj)
      max_r = max(p[0] for p in obj)
      max_height += (max_r - min_r + 1)
    
    max_width = 0
    for obj in filtered_objects:
      min_c = min(p[1] for p in obj)
      max_c = max(p[1] for p in obj)
      if (max_c - min_c + 1) > max_width:
        max_width = (max_c - min_c + 1)

    output_grid = np.zeros((max_height, max_width), dtype=int)


    # 4. Stack and Position
    current_row = 0
    for obj in filtered_objects:
        #find min row and col for object
        min_r = min(p[0] for p in obj)
        min_c = min(p[1] for p in obj)
        
        for r, c in obj:
            output_grid[r - min_r + current_row, c - min_c] = 3
        current_row += (max(p[0] for p in obj) - min_r + 1) #update for next object

    return output_grid.tolist()
```
