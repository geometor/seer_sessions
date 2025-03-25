"""
Transform the input grid by extracting regions defined by key colors and their neighbors, then compressing and arranging these regions into a smaller output grid.
"""

import numpy as np

def find_objects(grid, background_color):
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors
    
    def dfs(r, c, color, object_coords):
        if (r, c) in visited or grid[r, c] != color:
            return
        visited.add((r, c))
        object_coords.append((r, c))
        for nr, nc in get_neighbors(r, c):
            dfs(nr, nc, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != background_color and (r, c) not in visited:
                object_coords = []
                dfs(r, c, color, object_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(object_coords)

    return objects

def compress_object(object_coords):
    rows = sorted(list(set([r for r, c in object_coords])))
    cols = sorted(list(set([c for r, c in object_coords])))
    
    compressed_rows = []
    compressed_cols = []
    
    
    i = 0
    while i < len(rows):
        compressed_rows.append(rows[i])
        i += 1
            
    i = 0
    while i < len(cols):
        compressed_cols.append(cols[i])
        i += 1

    row_map = {r: i for i, r in enumerate(compressed_rows)}
    col_map = {c: i for i, c in enumerate(compressed_cols)}

    compressed_coords = []

    for r, c in object_coords:
        compressed_coords.append( (row_map[r], col_map[c]) )
    
    
    return compressed_coords, len(compressed_rows), len(compressed_cols)

def get_bounding_box(coords):
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    grid = np.array(input_grid)
    rows, cols = grid.shape
    background_color = grid[0, 0]

    objects = find_objects(grid, background_color)
    
    output_regions = {}
    max_row_offset = 0
    
    for color in sorted(objects.keys()):
        color_objects = objects[color]
        
        for obj_coords in color_objects:      
            compressed_coords, num_rows, num_cols = compress_object(obj_coords)

            if color not in output_regions:
               output_regions[color] =  (compressed_coords, num_rows, num_cols)
            else:
              # update
              prev_coords, prev_rows, prev_cols = output_regions[color]

              all_coords = prev_coords + compressed_coords

              _, updated_rows, updated_cols = compress_object(all_coords)
              updated_coords,_,_ = compress_object(all_coords)

              output_regions[color] = (updated_coords, updated_rows, updated_cols)

    
    total_rows = 0
    max_width = 0
    for color in output_regions:
        _, num_rows, num_cols = output_regions[color]
        total_rows = max(total_rows, num_rows)
        max_width += num_cols


    output_grid = np.full((total_rows, max_width), background_color, dtype=int)


    col_offset = 0
    for color in sorted(output_regions.keys()):
      compressed_coords, num_rows, num_cols = output_regions[color]
      for r, c in compressed_coords:
          output_grid[r, c + col_offset] = color
      col_offset += num_cols


    return output_grid.tolist()