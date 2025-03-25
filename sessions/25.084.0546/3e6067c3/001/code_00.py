"""
1.  **Identify Objects:** Treat contiguous regions of the same non-background color (non-8) as distinct objects.
2.  **Background Fill:**
    *   Scan the input grid.
    *   When a non-8 pixel is adjacent (horizontally or vertically, not diagonally) to an 8 (background) pixel, and it is part of a multi-pixel object of that color within its row :
        * Duplicate that object color in all adjacent locations
    * If a single color region exists on a previous row, check if that extends on to the current row. If not, then create a new object with the same pixels as background.

3.  **Preserve Special Row:** The row containing single instances of colors 2-9 (usually the last row) is copied to the output without modification.
4.  **Preserve Background:** Rows that are all background (all 8s) are copied without change, except in cases intersecting objects identified in step 2.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of the same color in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited and grid[row, col] != 8:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append((grid[row, col], obj))  # Store color and object pixels
    return objects

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    input_grid = np.array(input_grid)  # Ensure we're working with a NumPy array
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    objects = find_objects(input_grid)

    # Background Fill and Object Replication
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 8:
                for color, obj_pixels in objects:
                    for pixel_r, pixel_c in obj_pixels:                       
                        if (abs(r - pixel_r) + abs(c - pixel_c) == 1) and len([(pr,pc) for pr,pc in obj_pixels if pr == pixel_r]) > 1:
                            output_grid[r,c] = color
                            break

    # Handle expansion from previous rows.
    for r in range(1, rows):
      for c in range(cols):
        if output_grid[r,c] == 8:
            
          above_color = output_grid[r-1,c]
          if above_color != 8:
            # Check if there are any objects on current row with same color
            found = False
            for color, obj_pixels in objects:
                for pixel_r, pixel_c in obj_pixels:
                  if pixel_r == r and color == above_color:
                    found=True
                    break

            if not found: # if not found extend the above color to the background
                output_grid[r,c] = above_color
    

    return output_grid.tolist()