"""
1.  **Identify the gray line:** Find the vertical line of gray (5) pixels in the input grid.
2.  **Remove the gray line:** The output will not include this.
3.  **Identify the colored objects** the objects on the left of the gray line
4.  **Preserve and Crop:** For each colored object, keep only the pixels that are *directly adjacent* (horizontally or vertically, not diagonally) to the gray line. Remove all other parts.
5.  **Construct Output:** Create the output grid by arranging the preserved portions of the colored objects, maintaining their relative vertical positions from the input grid. The width of the output will be the maximum x value of any of the colored objects, excluding any part which was to the right of a preserved pixel.
"""

import numpy as np

def find_gray_line(grid):
    """Finds the vertical line of gray (5) pixels."""
    rows, cols = grid.shape
    for j in range(cols):
        is_gray_line = True
        for i in range(rows):
            if grid[i, j] != 5:
                is_gray_line = False
                break
        if is_gray_line:
            return j
    return -1  # Should not happen, based on problem description


def get_objects(grid):
     """Find contiguous blocks of non-background pixels."""
     rows, cols = grid.shape
     visited = np.zeros((rows, cols), dtype=bool)
     objects = []

     def is_valid(r, c):
         return 0 <= r < rows and 0 <= c < cols

     def dfs(r, c, color, obj_pixels):
         if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
             return
         visited[r, c] = True
         obj_pixels.append((r, c))
         for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
             dfs(r + dr, c + dc, color, obj_pixels)

     for r in range(rows):
         for c in range(cols):
             if grid[r, c] != 0 and not visited[r, c]:
                 obj_pixels = []
                 dfs(r, c, grid[r, c], obj_pixels)
                 objects.append(obj_pixels)
     return objects
def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    gray_line_col = find_gray_line(input_grid)
    objects = get_objects(input_grid)

    # Determine output grid width
    max_x = 0
    for obj in objects:
        for r, c in obj:
           if c < gray_line_col:
               max_x = max(max_x, c)


    output_grid = np.zeros((input_grid.shape[0], max_x + 1), dtype=int)


    # change output pixels - preserve parts of objects
    for obj in objects:
      for r, c in obj:
        if c < gray_line_col: # only consider objects left to the gray line
          is_adjacent = False
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < input_grid.shape[0] and nc == gray_line_col and input_grid[nr,nc] == 5:
              is_adjacent = True
              break
          if is_adjacent:
            output_grid[r,c] = input_grid[r,c]


    return output_grid.tolist()