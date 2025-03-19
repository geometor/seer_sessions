"""
The input grid is transformed into a smaller output grid by extracting and simplifying colored regions. Yellow (4) regions are reduced to their corner pixels. Orange (7) and Green (3) regions are merged if vertically adjacent or overlapping, forming simplified, connected shapes. The final output grid is condensed, removing empty white rows and adjusting the width.
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

def transform(input_grid):
    # initialize output_grid
    
    # 1. Identify Colored Regions.
    yellow_regions = get_regions(input_grid, 4)
    orange_regions = get_regions(input_grid, 7)
    green_regions = get_regions(input_grid, 3)

    # Find min/max rows/cols
    min_row = input_grid.shape[0]
    max_row = -1
    min_col = input_grid.shape[1]
    max_col = -1

    all_colored_pixels = []

    for region in yellow_regions:
      for r,c in region:
        all_colored_pixels.append((r,c))
    for region in orange_regions:
      for r,c in region:
        all_colored_pixels.append((r,c))
    for region in green_regions:
      for r,c in region:
        all_colored_pixels.append((r,c))


    for r,c in all_colored_pixels:
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)

    
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col+1), dtype=int)

    # 2. Condense and Extract:

    # Yellow (4): Extract corners
    for region in yellow_regions:
        rows, cols = zip(*region)  # Unzip the (row, col) pairs
        
        # Find corners
        
        top_row_pixels = [(r,c) for r,c in region if r == min(rows)]
        bottom_row_pixels = [(r,c) for r,c in region if r == max(rows)]
        left_col_pixels = [(r,c) for r,c in region if c == min(cols)]
        right_col_pixels = [(r,c) for r,c in region if c == max(cols)]
    
        # find intersection between them to find conrners
        corners = set(top_row_pixels).intersection(set(left_col_pixels))
        corners = corners.union(set(top_row_pixels).intersection(set(right_col_pixels)))
        corners = corners.union(set(bottom_row_pixels).intersection(set(left_col_pixels)))
        corners = corners.union(set(bottom_row_pixels).intersection(set(right_col_pixels)))

        for r,c in corners:
          output_grid[r - min_row, c - min_col] = 4


    # Orange and Green: Merge
    combined_orange = []
    for region in orange_regions:
      combined_orange.extend(region)

    combined_green = []
    for region in green_regions:
        combined_green.extend(region)

    orange_rows, orange_cols = zip(*combined_orange) if combined_orange else ([],[])
    if orange_rows:  # Make sure there are elements
        min_orange_row, max_orange_row = min(orange_rows), max(orange_rows)
        min_orange_col, max_orange_col = min(orange_cols), max(orange_cols)
        for r in range(min_orange_row, max_orange_row + 1):
            for c in range(min_orange_col, max_orange_col + 1):
                if (r,c) in combined_orange:
                    output_grid[r - min_row, c-min_col] = 7
                
    
    green_rows, green_cols = zip(*combined_green) if combined_green else ([],[])
    if green_rows:  # Make sure there are elements
      min_green_row, max_green_row = min(green_rows), max(green_rows)
      min_green_col, max_green_col = min(green_cols), max(green_cols)
      for r in range(min_green_row, max_green_row + 1):
          for c in range(min_green_col, max_green_col + 1):
            if (r,c) in combined_green:
              output_grid[r - min_row, c-min_col] = 3
    

    return output_grid