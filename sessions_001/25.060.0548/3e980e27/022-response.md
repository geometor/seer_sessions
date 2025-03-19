# 3e980e27 • 022 • example_4 • investigate_coder

---
```python
"""
Replicates and repositions colored regions within the grid. Yellow and a neighboring red structure is copied and moved down-left; a blue/green structure is copied, expanded, and moved up.
"""

import numpy as np

def find_object(grid, colors):
    """Finds a connected region of specified colors and returns its bounding box and pixels."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    object_pixels = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] not in colors:
            return
        visited[r, c] = True
        object_pixels.append((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        dfs(r + 1, c + 1)
        dfs(r - 1, c-1)
        dfs(r+1, c-1)
        dfs(r-1,c+1)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in colors and not visited[r, c]:
                dfs(r, c)
                if object_pixels:  # Ensure object was found
                    min_r = min(p[0] for p in object_pixels)
                    max_r = max(p[0] for p in object_pixels)
                    min_c = min(p[1] for p in object_pixels)
                    max_c = max(p[1] for p in object_pixels)
                    return (min_r, min_c, max_r, max_c), object_pixels
    return None, []

def get_neighbor_pixel(grid, object_pixels, neighbor_color):
    rows, cols = grid.shape
    neighbor = None
    for r,c in object_pixels:
        for dr, dc in [(0,1),(1,0), (0,-1),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]:
            nr, nc = r+dr, c + dc
            if 0<= nr < rows and 0 <= nc < cols and grid[nr, nc] == neighbor_color:
                neighbor = (nr, nc)
                return neighbor
    return None

def translate_object(grid_shape, object_pixels, dr, dc):
    """Translates object pixels by dr, dc."""
    translated_pixels = []
    for r, c in object_pixels:
        translated_pixels.append((r + dr, c + dc))
    return translated_pixels

def place_object(grid, object_pixels, color_map):
    for r, c in object_pixels:
        if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
            grid[r,c] = color_map[(r,c)]


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Objects
    yellow_bbox, yellow_pixels = find_object(input_grid, [4])
    red_pixel = get_neighbor_pixel(input_grid, yellow_pixels, 2)
    if red_pixel:
        yellow_pixels.append(red_pixel)
    
    color_map_yellow = {}
    for r,c in yellow_pixels:
        color_map_yellow[(r,c)] = input_grid[r,c]

    blue_green_bbox, blue_green_pixels = find_object(input_grid, [1, 3])
    color_map_bg = {}
    for r,c in blue_green_pixels:
        color_map_bg[(r,c)] = input_grid[r,c]

    # 2. Replicate and Translate Yellow
    yellow_dr = (blue_green_bbox[2] - yellow_bbox[0] + 1 )
    yellow_dc = -(yellow_bbox[1]-blue_green_bbox[1] )

    translated_yellow_pixels = translate_object(input_grid.shape, yellow_pixels, yellow_dr, yellow_dc)
    
    new_color_map_yellow={}
    for (orow, ocol), (nrow, ncol) in zip(yellow_pixels, translated_yellow_pixels):
        new_color_map_yellow[(nrow,ncol)] = color_map_yellow[(orow, ocol)]
    
    place_object(output_grid, translated_yellow_pixels, new_color_map_yellow)

    # 3. Replicate, Insert, Translate Blue/Green
    #   Replicate
    
    blue_green_pixels_expanded = []
    min_c = min(c for _,c in blue_green_pixels)
    new_color_map_bg = {}

    for r,c in blue_green_pixels:
        new_color_map_bg[(r,c)] = color_map_bg[(r,c)]
        if c == min_c:
           blue_green_pixels_expanded.append((r,c))
           new_color_map_bg[(r, c - 1)] = 1 #insert blue to left of every left-most column element
           blue_green_pixels_expanded.append((r, c - 1))

        else:
           blue_green_pixels_expanded.append((r,c))


    blue_green_dr = -(blue_green_bbox[0] - yellow_bbox[2] + 1) # move up to below original yellow
    blue_green_dc =  - (yellow_bbox[3] - yellow_bbox[1] + 1) * 2 #align to left edge of new yellow structure

    translated_blue_green_pixels = translate_object(input_grid.shape, blue_green_pixels_expanded, blue_green_dr, blue_green_dc)
    new_translated_bg_map = {}

    for (orow, ocol), (nrow, ncol) in zip(blue_green_pixels_expanded, translated_blue_green_pixels):
      if (orow, ocol) in new_color_map_bg:
          new_translated_bg_map[(nrow, ncol)] = new_color_map_bg[(orow, ocol)]

    place_object(output_grid, translated_blue_green_pixels, new_translated_bg_map )



    # 4. Background (fill in unchanged pixels)
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r,c] == 0:
              output_grid[r,c] = input_grid[r,c]

    return output_grid
```
