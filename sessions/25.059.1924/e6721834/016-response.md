# e6721834 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify the Region of Interest: Focus on the right half of the input grid (the azure (8) region).
2. Isolate Objects: Within the azure region, identify the distinct colored objects: the blue (1) object, the red (2) pixels, and the magenta (6) pixel.
3. Crop and Extract: Crop the input grid, discarding all columns starting at the vertical mid-point.
4. Remove all background pixels in the extracted section (azure pixels)
5. Reconstruct, maintaining the relative positions and colors. The final result is the cropped section containing the remaining object(s).
"""

import numpy as np

def get_objects(grid, background_color):
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, object_coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        object_coords.append((r, c))
        dfs(r + 1, c, color, object_coords)
        dfs(r - 1, c, color, object_coords)
        dfs(r, c + 1, color, object_coords)
        dfs(r, c - 1, color, object_coords)


    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != background_color:
                color = grid[r, c]
                object_coords = []
                dfs(r, c, color, object_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(object_coords)
    return objects
def transform(input_grid):
    # initialize output_grid
    rows, cols = input_grid.shape
    mid_col = cols // 2
    cropped_grid = input_grid[:, :mid_col]
    output_grid = np.copy(cropped_grid)
    
    #get objects in the right half
    right_half = input_grid[:, mid_col:]
    objects = get_objects(right_half, 8)

    #put right objects in right place
    object_map = {}
    for color, obj_list in objects.items():
        for obj_coords in obj_list:
            for r_offset, c_offset in obj_coords:
                r = r_offset
                c = c_offset
                
                if (r,c) not in object_map:
                    object_map[(r,c)] = []

                object_map[(r,c)].append(color)

    for (r,c), color_list in object_map.items():
        #handle multiple colors? should only be 1 per pixel
        output_grid[r,c] = color_list[0]

    return output_grid
```
