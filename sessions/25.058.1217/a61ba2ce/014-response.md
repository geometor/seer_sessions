# a61ba2ce • 014 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous blocks of non-black (non-zero) colored pixels in the input grid. Each block is an object.
2.  **Determine Output Grid Size**: Count the *unique* colors of the objects identified in step 1. Let the number of unique object colors be *n*. The output grid will be *k* x *k*, where k is determined as follows:
      * n = 1: k = 1
      * n = 2, 3, or 4: k = 2
      * n > 4: Not handled in this version
3. **Assign Quadrants**: Create a mapping for up to 4 colors for placement into a 2x2 grid. Use this order of precedence: Blue (1), Azure (8), Yellow (4), Red (2).
    - If Blue (1) exists, the top-left quadrant (0,0) represents Blue.
    - If Azure (8) exists, the top-right quadrant represents Azure. If there is only one unique color and it is Azure, its position should be (0, 0).
    - If Yellow (4) exists, the bottom-left quadrant represents Yellow. If there is only one unique color and it is Yellow, its position should be (0, 0).
    - If Red (2) exists, the bottom-right quadrant represents Red. If there is only one unique color and it is Red, its position should be (0, 0).
4.  **Object Placement:** Place each identified object into its designated quadrant based on the color mapping in step 3. The objects should be placed starting at the top-left of their quadrant, maintaining their original shape and size. Objects of the same color that are placed into the same quadrant should be packed together.
5. **Fill Empty Quadrants**: If a quadrant does not have a corresponding object color, leave the quadrant empty (filled with zeros, black).
6. **Handle Single color edge case**: If n=1, the output is 1x1 and is just the single color.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                if obj_pixels:
                    objects.append({'color': grid[row, col], 'pixels': obj_pixels})
    return objects

def transform(input_grid):
    # Find objects
    objects = find_objects(input_grid)

    # Determine output grid size
    unique_colors = sorted(list(set([obj['color'] for obj in objects])))
    n = len(unique_colors)
    k = 1 if n == 1 else 2 if n <= 4 else None  # Handle up to 4 unique colors

    if k is None:
        return None  # Not handling cases with more than 4 unique colors

    # initialize output_grid
    output_grid = np.zeros((k, k), dtype=int)

    # Assign quadrants
    quadrant_map = {}  # color -> (row_start, col_start)
    if n == 1:
        quadrant_map[unique_colors[0]] = (0,0) # single color
    else: # n == 2,3,4
        if 1 in unique_colors:  # Blue
            quadrant_map[1] = (0, 0)
        if 8 in unique_colors:  # Azure
            quadrant_map[8] = (0, 1) if 1 in quadrant_map else (0,0)
        if 4 in unique_colors:  # Yellow
            quadrant_map[4] = (1, 0) if 8 in quadrant_map or 1 in quadrant_map else (0,0)
        if 2 in unique_colors:  # Red
            quadrant_map[2] = (1, 1) if 4 in quadrant_map or 8 in quadrant_map or 1 in quadrant_map else (0,0)
    
    # Place objects in quadrants
    for obj in objects:
        color = obj['color']
        pixels = obj['pixels']

        if color in quadrant_map:
            quadrant_row, quadrant_col = quadrant_map[color]

            # find top left of object in its own coordinates
            min_row = min(p[0] for p in pixels)
            min_col = min(p[1] for p in pixels)

            # Place pixels in quadrant
            for r, c in pixels:
                # use delta from min row, col
                dr = r - min_row
                dc = c - min_col
                row_in_quadrant = quadrant_row + dr
                col_in_quadrant = quadrant_col + dc

                if 0 <= row_in_quadrant < k and 0 <= col_in_quadrant < k:
                    output_grid[row_in_quadrant, col_in_quadrant] = color

    return output_grid
```
