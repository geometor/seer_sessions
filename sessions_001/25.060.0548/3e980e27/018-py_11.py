"""
1.  **Identify Objects:** Identify all contiguous blocks of non-white pixels in the input grid. Each block is an object.
2.  **Determine Dividing Line:**  A vertical dividing line exists in the grid.  It is approximated by the center column (`input_grid.shape[1] // 2`).
3.  **Object Transformations:**
    *   Objects to the *left* of the dividing line with colors green (3) and azure (8) are removed.
    *   The object to the *right* of the dividing line with color red (2) is moved upwards. The number of rows it moves up is consistent.
    *   The object to the *right* of the dividing line with color yellow (4) is moved to the *left* of the dividing line and significantly increases in size, forming a vertical bar.
    * If an object already exists at the target location, adjust the location to avoid overwriting.
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

        # Objects to the left with colors green (3) and azure (8) are removed.
        if is_left and (color == 3 or color == 8):
            continue

        # The object to the right with color red (2) moves up
        if is_right and color == 2:
            min_row = min(r for r, _ in coords)
            #Consistent upward movement noted across examples
            new_row = min_row - (min_row- (rows//4)) if rows//4 < min_row else 0  

            for r, c in coords:
              if new_row >=0:
                output_grid[new_row, c] = color

        # The object to the right with color yellow(4) moves to left and expands
        if is_right and color == 4:
            new_col_start = 0
            new_col_end = 2  # expand to 3 cols
            for r in range(rows-len(coords)-1, rows):
                for c in range(new_col_start, new_col_end +1):
                   output_grid[r,c] = 4

    # transfer remaining color (2) objects
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 2:
          if sum(output_grid[r]) == 0:
            output_grid[r,c] = 2

    return output_grid