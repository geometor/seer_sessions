"""
The transformation identifies distinct colored regions in the input grid and expands them horizontally and vertically until the edges of the regions are adjacent.
"""

import numpy as np

def find_colored_regions(grid):
    # Find all distinct, contiguous blocks of non-zero pixels.
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, color, region):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        region.append((row, col))
        dfs(row + 1, col, color, region)
        dfs(row - 1, col, color, region)
        dfs(row, col + 1, color, region)
        dfs(row, col - 1, color, region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                color = grid[row, col]
                region = []
                dfs(row, col, color, region)
                regions.append((color, region))
    return regions

def expand_region(grid, region, color):
  # Expand the region horizontally and vertically.
  new_region = region.copy()
  for r, c in region:
    # Expand up
    if r > 0 and grid[r-1,c] == 0:
        new_region.append((r - 1, c))
    # Expand down
    if r < grid.shape[0] - 1 and grid[r+1,c] == 0:
        new_region.append((r + 1, c))
    # Expand left
    if c > 0 and grid[r,c-1] == 0:
        new_region.append((r, c - 1))
    # Expand right
    if c < grid.shape[1] -1 and grid[r,c+1] == 0:
        new_region.append((r, c+1))

  return new_region

def check_adjacency(regions):
  # returns true if all regions are adjacent
    for i in range(len(regions)):
        color1, region1 = regions[i]
        for r1, c1 in region1:
            adjacent = False
            for j in range(len(regions)):
                if i == j:
                    continue
                color2, region2 = regions[j]

                for r2, c2 in region2:
                  # check up, down, left, right
                  if (r1 == r2 + 1 and c1 == c2):
                      adjacent = True
                  if (r1 == r2 - 1 and c1 == c2):
                      adjacent = True
                  if (r1 == r2 and c1 == c2 + 1):
                      adjacent = True
                  if (r1 == r2 and c1 == c2 - 1):
                      adjacent = True
            if not adjacent:
              return False
    return True


def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find colored regions.
    regions = find_colored_regions(input_grid)
    
    # Continue to expand and ceck until all are adjacent
    adjacent = False
    while(not adjacent):
        
        new_regions = []
        # Expand each regions
        for color, region in regions:
            new_region = expand_region(output_grid, region, color)
            new_regions.append((color, new_region))

        # Update output grid
        output_grid = np.zeros_like(input_grid)

        # Set color values in output
        for color, region in new_regions:
            for r, c in region:
                output_grid[r, c] = color

        # Check for full adjacency between regions
        adjacent = check_adjacency(new_regions)

        # update regions
        regions = new_regions

    return output_grid