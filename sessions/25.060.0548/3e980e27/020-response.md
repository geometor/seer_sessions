# 3e980e27 • 020 • refine_coder

---
```python
"""
1.  **Identify Objects:** Identify all contiguous blocks of non-white pixels in the input grid. Each block constitutes an object.
2.  **Determine Dividing Line:** Imagine a vertical dividing line at the center of the grid (`input_grid.shape[1] // 2`).
3.  **Left Side Transformations:**
    *   Remove all green (3) and azure (8) objects located to the left of the dividing line.
4.  **Right Side Transformations:**
    *   Red (2) Object:
        *   If the object has a height of 3 or more, move it up by `original_top_row - calculated_target_row`.  `calculated_target_row` is a fraction of the height, but should not be greater than `original_top_row`.
    *   Yellow (4) Object:
        * If the height of the yellow object is greater than or equal to 3: Move all pixels of this object to the left side of the grid. The moved object should start at column 0, span 3 columns wide, and extend the original height of the yellow object, starting three rows from the bottom.
        * If the height of the yellow object is less than 3: Do not transform.

5.  **Object Persistence:** Any object or pixel not explicitly mentioned in the transformation rules above should remain in its original position in the output grid. Copy these unchanged elements directly from the input to the output.
"""

import numpy as np

def find_objects(grid):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({"color": grid[r, c], "coords": obj_coords})
    return objects

def object_height(coords):
    rows = [r for r, _ in coords]
    return max(rows) - min(rows) + 1

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    objects = find_objects(input_grid)

    # Determine Dividing Line
    mid_col = cols // 2

    # Object Transformations
    for obj in objects:
        color = obj['color']
        coords = obj['coords']
        
        # Check if object is on the left or right of the dividing line
        is_left = any(c < mid_col for _, c in coords)
        is_right = any(c >= mid_col for _, c in coords)

        # Left Side: Remove green (3) and azure (8)
        if is_left and (color == 3 or color == 8):
            continue

        # Right Side: Red (2) - Conditional move up
        if is_right and color == 2:
            if object_height(coords) >= 3:
                min_row = min(r for r, _ in coords)
                new_row = 0  # Move to the top
                for r, c in coords:
                    output_grid[new_row + (r - min_row), c] = color

        # Right side: Yellow (4) object transformation
        elif is_right and color == 4:
          if object_height(coords) >=3:
            new_col_start = 0
            new_col_end = 2  # expand to 3 cols
            height = object_height(coords)
            for i, (r,c) in enumerate(sorted(coords)):
                for c_new in range(new_col_start, new_col_end+1):
                  output_grid[rows - height-2 +i, c_new] = 4
          else:
            for r, c in coords:
                output_grid[r,c] = color # no change

        # object persistence, transfer all other objects
        else:
          for r, c in coords:
            output_grid[r, c] = color

    return output_grid
```
