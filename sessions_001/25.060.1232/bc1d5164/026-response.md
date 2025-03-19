# bc1d5164 • 026 • refine_coder

---
```python
"""
The transformation identifies objects of a specific color and combines or extracts them based on their spatial relationship.

1.  **Identify Objects:** Find all contiguous regions (objects) of the same color, excluding color 0 (background).

2.  **Color-Specific Rules:**
    *   **If color 4 (yellow) is the only color present:** Reduce the height of the grid by 1, keeping the width the same. Fill the output grid with color 4.
    *   **If color 1 (blue) is present and there are two 2x2 blue objects:** Output a single 2x2 grid filled with blue at position (0,0).
    *   **If there are two blue 2x2 objects:** Create two 2x2 blue objects, and position with offset (0,0) and (0,3).
    *   **If color 2 (red) is present:**
        *   Combine any red objects that share the same top row or are adjacent into a single rectangular object.

3.  **Default:** If no rules apply, no change (or return empty grid).
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.  An object is a group of
    contiguous pixels of the same color.
    Returns a list of objects, where each object is a dictionary
    containing: color, and pixel coordinates.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_pixels):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        obj_pixels.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            color = grid[r][c]
            if color != 0 and (r, c) not in visited:
                obj_pixels = []
                dfs(r, c, color, obj_pixels)
                if obj_pixels:
                    objects.append({"color": color, "pixels": obj_pixels})
    return objects

def bounding_box(pixels):
    """
    Calculates the smallest bounding box around a set of pixels.
    """
    if not pixels:
        return None
    rows, cols = zip(*pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return (min_row, min_col), (max_row, max_col)

def is_2x2_rectangle(obj):
    """Checks if an object is a 2x2 rectangle."""
    top_left, bottom_right = bounding_box(obj['pixels'])
    if top_left is None or bottom_right is None:
        return False
    return (bottom_right[0] - top_left[0] == 1) and (bottom_right[1] - top_left[1] == 1)

def combine_objects(objects):
    """Combines list of objects of same color into one object."""
    if not objects:
      return None

    pixels = []
    for obj in objects:
      pixels.extend(obj['pixels'])
    
    color = objects[0]['color']

    return {'color': color, 'pixels': pixels}

def transform(input_grid):
    """Transforms the input grid according to the rules described above."""
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)
    
    # Color 4 (yellow) rule:
    if len(objects) == 1 and objects[0]['color'] == 4:
        height, width = input_grid.shape
        output_grid = np.full((height - 1, width), 4, dtype=int)
        return output_grid.tolist()

    # Color 1 (blue) rules:
    blue_objects = [obj for obj in objects if obj['color'] == 1]
    if len(blue_objects) == 2:
        all_2x2 = all(is_2x2_rectangle(obj) for obj in blue_objects)
        if all_2x2:
          # get top left coords
          coords = []
          for obj in blue_objects:
              top_left, _ = bounding_box(obj['pixels'])
              coords.append(top_left)
          coords.sort()

          output_grid = np.zeros((4,6), dtype=int)
        
          # recreate each object with offset
          for i, (r,c) in enumerate(coords):
              # top left at (0,0) and (0,3)
              out_r = 0
              out_c = i * 3
              for dr in range(2):
                  for dc in range(2):
                    output_grid[out_r + dr, out_c + dc] = 1
          return output_grid.tolist()
            
    # Color 2 (red) rule:
    red_objects = [obj for obj in objects if obj['color'] == 2]
    if red_objects:
        combined_object = combine_objects(red_objects)
        top_left, bottom_right = bounding_box(combined_object['pixels'])
        min_row, min_col = top_left
        max_row, max_col = bottom_right

        # create output grid
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        output_grid = np.zeros((height, width), dtype=int)

        # fill in pixels inside the bounding box,
        for r, c in combined_object['pixels']:
            output_grid[r-min_row, c-min_col] = 2
        return output_grid.tolist()

    # Default:
    return input_grid.tolist()  # No change
```
