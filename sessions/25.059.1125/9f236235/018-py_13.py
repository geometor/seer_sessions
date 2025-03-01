"""
1.  **Identify Regions:** Divide the input grid into contiguous color regions. A region is defined as a group of adjacent pixels of the same color.
2.  **Locate Key Regions:**
    * Find the region that occupies the majority of the top and/or left portion.
    * Find the region that occupies the center-right vertically.
3.  **Sample Colors:**
    * Sample the color from the bottom-right corner of the "top/left" region, use black (0) if this is the green (3) region.
    * Sample the color from the bottom-right corner of the "middle-right" region.
    * If there is a region that spans the bottom left, sample that.
4.  **Construct Output Grid:** Create a 3x3 output grid.
    *   Place the sampled color from the top/left at the top-left (0, 0).
    *   Place the sample color from the middle-right to the top-right (0,1) and span 2 columns.
    *   If the bottom-left sample exists, put this at (2,0)
"""

import numpy as np

def find_regions(grid):
    # simple region finding, assumes no nested regions
    regions = {}
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, color, region_coords):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != color:
            return
        visited.add((r, c))
        region_coords.append((r, c))
        dfs(r + 1, c, color, region_coords)
        dfs(r - 1, c, color, region_coords)
        dfs(r, c + 1, color, region_coords)
        dfs(r, c - 1, color, region_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r][c]
                region_coords = []
                dfs(r, c, color, region_coords)
                if region_coords:
                    regions[color] = region_coords

    return regions

def get_bottom_right(region_pixels):
     #find bottom right
    return max(region_pixels, key=lambda item: (item[0], item[1]))

def get_top_left_region(grid, regions):
    # Find the region that contains the top-left corner
    top_left_color = grid[0][0]
    return regions.get(top_left_color)

def get_middle_right_region(grid, regions):
   # Find a region on the middle-right side
    rows, cols = len(grid), len(grid[0])
    mid_row = rows // 2
    for c in range(cols - 1, cols // 2, -1):  # Iterate from right to center
        color = grid[mid_row][c]
        if color in regions:
             # check to see this region spans vertically
            region_pixels = regions[color]
            min_row = min(region_pixels, key=lambda item: item[0])[0]
            max_row = max(region_pixels, key=lambda item: item[0])[0]
            if max_row - min_row + 1 == rows:
                return regions[color]

    return None #should not happen

def get_bottom_left_region(grid, regions):
   # Find a region on the bottom-left side
    rows, cols = len(grid), len(grid[0])
    
    for r in range(rows -1, -1, -1):
        for c in range(0, cols // 2):
            color = grid[r][c]
            if color in regions:
                return regions[color]

    return None #should not happen

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)
    grid = np.array(input_grid)

    # find the three regions, assume input is always 11 x 11 and the three regions are there
    regions = find_regions(input_grid)
    
    # get top/left region
    top_left_region_pixels = get_top_left_region(grid, regions)
    if top_left_region_pixels:
        #find bottom right
        bottom_right = get_bottom_right(top_left_region_pixels)
        top_left_color = grid[bottom_right[0]][bottom_right[1]]
        output_grid[0][0] = 0 if top_left_color == 3 else top_left_color

    # get middle/right region
    middle_right_region_pixels = get_middle_right_region(grid, regions)
    if middle_right_region_pixels:
        #find bottom right
        bottom_right = get_bottom_right(middle_right_region_pixels)
        output_grid[0:2, 1:3] =  grid[bottom_right[0]][bottom_right[1]]

    # get bottom/left region
    bottom_left_region_pixels = get_bottom_left_region(grid, regions)
    if bottom_left_region_pixels:
        #find bottom right
        bottom_right = get_bottom_right(bottom_left_region_pixels)
        output_grid[2][0] =  grid[bottom_right[0]][bottom_right[1]]

    return output_grid