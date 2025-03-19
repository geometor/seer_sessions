"""
The transformation identifies large color regions in the input grid, samples a single color from a specific location (bottom-right) within each of the three regions, and constructs a smaller 3x3 output grid using these sampled colors, arranging according to the location of the sample.
"""

import numpy as np

def find_regions(grid):
    # very simple region finding, assumes no nested regions
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
                

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # find the three regions, assume input is always 11 x 11 and the three regions are there
    grid = np.array(input_grid)
    regions = find_regions(input_grid)
    
    # get bottom right of each region, and put the value in the correct location in output
    
    #top left
    top_left_region_color = input_grid[0][3] #red
    top_left_pixels = regions.get(top_left_region_color, None)
    if top_left_pixels:
        #find bottom right
        bottom_right = max(top_left_pixels, key=lambda item: (item[0], item[1]))
        output_grid[0][0] = 0

    #bottom left
    bottom_left_region_color = input_grid[3][0] #blue
    bottom_left_pixels = regions.get(bottom_left_region_color, None)
    if bottom_left_pixels:
         #find bottom right
        bottom_right = max(bottom_left_pixels, key=lambda item: (item[0], item[1]))
        output_grid[2][0] = input_grid[bottom_right[0]][bottom_right[1]-1]
        
    #top right
    top_right_region_color = input_grid[0][8] #azure
    top_right_pixels = regions.get(top_right_region_color, None)

    if top_right_pixels:
        #find bottom right
        bottom_right = max(top_right_pixels, key=lambda item: (item[0], item[1]))

        # check for adjacent regions with the same color, continue checking until no more
        next_pixel = (bottom_right[0], bottom_right[1]+1)
        while next_pixel[1] < len(input_grid[0]) and input_grid[next_pixel[0]][next_pixel[1]] == top_right_region_color:
            bottom_right = next_pixel
            next_pixel = (bottom_right[0], bottom_right[1] + 1)
        output_grid[0:2, 1:3] =  input_grid[bottom_right[0]][bottom_right[1]]

     #bottom right
    bottom_right_region_color = input_grid[8][8] #yellow
    bottom_right_pixels = regions.get(bottom_right_region_color)

    if bottom_right_pixels:
          #find bottom right
        bottom_right = max(bottom_right_pixels, key=lambda item: (item[0], item[1]))
        output_grid[2][0] =  input_grid[bottom_right[0]][bottom_right[1]]


    return output_grid