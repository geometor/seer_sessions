"""
The transformation involves repositioning gray (5) regions relative to red (2) regions within the grid. Copies of each gray region are placed above and below the vertical extent of all red regions, while maintaining their original column positions. The remaining space is filled with black (0).
"""

import numpy as np

def find_regions(grid, color):
    """
    Finds all distinct regions of a specific color in the grid.

    Args:
        grid: The input numpy array.
        color: The color to search for.

    Returns:
        A list of regions, where each region is a list of (row, col) coordinates.
    """
    visited = set()
    regions = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_region):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_region.append((r, c))

        # Explore adjacent cells (4-connectivity)
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)

    return regions

def get_row_extents(regions):
    """Calculates the minimum and maximum row indices across all regions"""

    if not regions:
        return 0, -1  # No regions

    min_row = float('inf')
    max_row = float('-inf')

    for region in regions:
        for r, _ in region:
            min_row = min(min_row, r)
            max_row = max(max_row, r)

    return min_row, max_row

def transform(input_grid):
    """
    Transforms the input grid by repositioning gray regions relative to red regions.
    """
    grid = np.array(input_grid)
    output_grid = np.zeros_like(grid)

    # 1. Identify Red Regions
    red_regions = find_regions(grid, 2)

    # 2. Identify Gray Regions
    gray_regions = find_regions(grid, 5)

    # 3. Determine Row Placement (Vertical Extent of Red Regions)
    red_min_row, red_max_row = get_row_extents(red_regions)

    # 4. Reposition Gray Regions
    current_row_above = 0
    current_row_below = red_max_row + 1

    for gray_region in gray_regions:
        # Create two copies of the gray region

        # Place above
        for r, c in gray_region:
          height = max(r-get_row_extents([gray_region])[0],0) # original height
          output_grid[current_row_above + height, c] = 5

        # Place below
        for r,c in gray_region:
            height = max(r-get_row_extents([gray_region])[0],0)
            output_grid[current_row_below + height, c] = 5

        # move to the next available set of rows
        current_row_above += get_row_extents([gray_region])[1] - get_row_extents([gray_region])[0] + 1
        current_row_below += get_row_extents([gray_region])[1] - get_row_extents([gray_region])[0] + 1


    # add red regions
    for red_region in red_regions:
        for r, c in red_region:
          output_grid[r,c] = 2


    # 5. Fill Background (already initialized to 0, so no explicit action needed)

    return output_grid.tolist()