"""
The input grid is transformed by identifying and manipulating specific colored regions. Yellow (4) regions are reduced to their corner pixels. Orange (7) and Green (3) regions are combined, but treated as distinct entities if they are not directly adjacent.  The output grid contains the corner pixels of the yellow regions, and separate filled rectangles for each contiguous orange/green region. The output grid size is determined by the bounding box that encompasses all these elements.
"""

import numpy as np

def get_regions(grid, color):
    regions = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(row, col):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != color:
            return []

        visited.add((row, col))
        region = [(row, col)]

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            region.extend(dfs(row + dr, col + dc))
        
        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == color and (r,c) not in visited:
                regions.append(dfs(r,c))

    return regions

def get_corners(region):
    rows, cols = zip(*region)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    top_left = (min_row, min_col)
    top_right = (min_row, max_col)
    bottom_left = (max_row, min_col)
    bottom_right = (max_row, max_col)

    corners = set()
    if top_left in region:
        corners.add(top_left)
    if top_right in region:
        corners.add(top_right)
    if bottom_left in region:
        corners.add(bottom_left)
    if bottom_right in region:
        corners.add(bottom_right)
    return list(corners)

def get_bounding_box(region):
    if not region:
        return None

    rows, cols = zip(*region)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # 1. Identify Colored Regions.
    yellow_regions = get_regions(input_grid, 4)
    orange_regions = get_regions(input_grid, 7)
    green_regions = get_regions(input_grid, 3)

    # 2. Simplify Yellow Regions (Corners).
    simplified_yellow = []
    for region in yellow_regions:
        simplified_yellow.extend(get_corners(region))

    # 3. Treat Orange and Green regions separately, but combine adjacent ones
    combined_orange_green_regions = []
    
    # Create a combined list but keep regions distinct
    all_orange_green = []
    for region in orange_regions:
        all_orange_green.append(region)
    for region in green_regions:
        all_orange_green.append(region)
                
    # 4. Find bounding boxes for each distinct region (yellow corners, and each combined orange/green)
    boxes = []
    if simplified_yellow:
        yellow_bounding_box = get_bounding_box(simplified_yellow)
        if yellow_bounding_box:
            boxes.append(yellow_bounding_box)

    for og_region in all_orange_green:
      og_bounding_box = get_bounding_box(og_region)
      if og_bounding_box:
        boxes.append(og_bounding_box)

    if not boxes:
        return np.zeros((0, 0), dtype=int)

    # find the min and max of ALL the boxes:
    min_rows, max_rows, min_cols, max_cols = zip(*boxes)
    min_row = min(min_rows)
    max_row = max(max_rows)
    min_col = min(min_cols)
    max_col = max(max_cols)

    # 5. Create Output Grid based on combined bounding box
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    # 6. Populate output grid
    # Yellow corners
    for r, c in simplified_yellow:
        output_grid[r - min_row, c - min_col] = 4

    # Fill each orange/green region
    for og_region in all_orange_green:
        orange_green_rows, orange_green_cols = zip(*og_region)
        min_og_row = min(orange_green_rows)
        max_og_row = max(orange_green_rows)
        min_og_col = min(orange_green_cols)
        max_og_col = max(orange_green_cols)

        for r in range(min_og_row, max_og_row + 1):
            for c in range(min_og_col, max_og_col + 1):
                if (r, c) in og_region:
                    color = input_grid[r, c]  # original color
                    output_grid[r - min_row, c - min_col] = color
                    
    # 7. Return Output Grid
    return output_grid