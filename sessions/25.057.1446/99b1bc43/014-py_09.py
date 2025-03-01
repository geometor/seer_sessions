"""
Identifies distinct colored regions in the top-left quarter of the input grid (blue, yellow, and red), maps these colors to green, and reconstructs a 4x4 output grid preserving the relative positions of these regions, filling the rest with white.
"""

import numpy as np

def find_top_left_regions(grid):
    regions = {}
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, region_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        region_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, region_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color != 0: #ignore white
                    region_coords = []
                    dfs(r, c, color, region_coords)
                    
                    if len(region_coords) > 1 : # Consider only regions larger than single pixels for 2x2
                      min_r = min(coord[0] for coord in region_coords)
                      min_c = min(coord[1] for coord in region_coords)
                      max_r = max(coord[0] for coord in region_coords)
                      max_c = max(coord[1] for coord in region_coords)

                      # check if its in top-left
                      if max_r < rows//2 + rows%2  and max_c < cols//2 + cols % 2 : # accounts for odd size
                        regions[(min_r,min_c)] = (color, region_coords) # use top,left as key
    return regions

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Find regions in the top-left quarter of the input grid
    regions = find_top_left_regions(np.array(input_grid))
    
    # change output pixels
    color_map = {1: 3, 2: 3, 4: 3}  # blue, red, yellow to green
    for (r,c), (color, region_coords) in regions.items():
      
        # use first coord relative pos
        first_coord = region_coords[0]
        rel_r = first_coord[0] 
        rel_c = first_coord[1]

        mapped_color = color_map.get(color,0) # map or keep white

        if mapped_color != 0:
            output_grid[rel_r,rel_c] = mapped_color
            # handle 2xN shapes from top-left
            if len(region_coords) >= 3:
              second_coord = region_coords[1]
              output_grid[second_coord[0], second_coord[1]] = mapped_color

    return output_grid