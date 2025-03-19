# f35d900a • 002 • example_4 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Scan the input grid and identify all distinct, contiguous colored pixel groups (objects). Treat each isolated colored object.
2.  **Horizontal Expansion:** For each colored pixel in an object, a horizontal line with length 3 and the color of the object is created, where the original pixel is at the center of the line.
3. **Vertical Expansion:** For each colored pixel in an object, a vertical line with length 3 and the color of the object is created, where the original pixel is at the center of the line.
4.  **Mirroring:** If one object is to the left/right of the horizontal center of the input, its mirrored position will be on the right/left of the horizontal center of the output.
5.  **Create background:** After expansion/mirroring of objects, if there are empty pixels between and around the expanded pixels of the objects, a grey pixel (color 5) will be placed.
6.  **Fill Background:** Fill the remaining empty cells in the output grid with color 0 (white/blank).
"""

import numpy as np

def get_objects(grid):
    """Finds contiguous colored objects in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({'color': grid[r, c], 'coords': obj_coords})
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    objects = get_objects(input_grid)

    for obj in objects:
        color = obj['color']
        for r, c in obj['coords']:
            # Horizontal Expansion
            for i in range(-1, 2):
                if 0 <= c + i < cols:
                    output_grid[r, c + i] = color

            # Vertical Expansion
            for i in range(-1, 2):
                if 0 <= r + i < rows:
                    output_grid[r + i, c] = color

    # Mirroring and background insertion (5)
    for obj in objects:
      color = obj['color']
      for r,c in obj['coords']:
        center_col = cols // 2
        # original position
        orow = r
        ocol = c

        # Horizontal mirroring logic
        if ocol < center_col: # object in left side
          mirrored_c = center_col + (center_col - ocol -1)  if cols % 2 !=0 else center_col + (center_col - ocol -1) -1 # adjust mirrored pos based on grid width
          # fill expansion with original colors
          if mirrored_c < cols:
            for i in range(-1, 2):
                if 0 <= orow + i < rows:
                   output_grid[orow+i, mirrored_c] = color
            for i in range(-1, 2):
                if 0 <= mirrored_c + i < cols:
                    output_grid[orow, mirrored_c+i] = color

        elif ocol >= center_col: # object at or right side
          mirrored_c = center_col - (ocol-center_col + 1) if cols%2 != 0 else  center_col - (ocol-center_col)
          if mirrored_c >=0:
            for i in range(-1, 2):
                if 0 <= orow + i < rows:
                   output_grid[orow+i, mirrored_c] = color
            for i in range(-1, 2):
                if 0 <= mirrored_c + i < cols:
                    output_grid[orow, mirrored_c+i] = color


    # add grey background after expansion/mirroring
    for r in range(rows):
      for c in range(cols):
        if output_grid[r,c] == 0:
          # check neighbors
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1,1), (-1,-1), (1,-1), (-1,1)]: # check diagonals too
            nr, nc = r + dr, c+ dc
            if 0<= nr < rows and 0 <= nc < cols and output_grid[nr,nc] != 0:
              output_grid[r,c] = 5
              break # once marked as grey background skip


    return output_grid
```
