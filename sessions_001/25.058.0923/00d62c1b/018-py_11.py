"""
1.  **Identify Green Regions:** Locate all groups of contiguous green (value '3') pixels in the input grid.  Treat each group of connected green pixels as a separate region, even if they are not rectangular.
2.  **Enclose with Minimum Bounding Rectangle:** For *each* identified green region, find the smallest rectangle (a "bounding box") that completely encloses all pixels of that region. The sides of this rectangle must be parallel to the grid axes (no rotated rectangles).
3.  **Change Color Within Bounding Rectangles:** Change the color of all pixels within each of these minimum bounding rectangles from green ('3') to yellow ('4').
4.  **Output:** The output grid is identical to the input grid, except for the pixels within the bounding rectangles of the green regions, which are now yellow.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    # Find contiguous regions of a specified color
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def find_bounding_rectangle(region_coords):
    # Find the minimum bounding rectangle for a set of coordinates
    if not region_coords:
        return []
    min_row = min(r for r, _ in region_coords)
    max_row = max(r for r, _ in region_coords)
    min_col = min(c for _, c in region_coords)
    max_col = max(c for _, c in region_coords)
    
    rectangle_coords = []
    for row in range(min_row, max_row + 1):
      for col in range(min_col, max_col + 1):
        rectangle_coords.append((row,col))

    return rectangle_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)

    # Find contiguous green regions
    green_regions = find_contiguous_regions(grid, 3)

    # Find bounding rectangles for each region and change color
    for region in green_regions:
        rectangle_coords = find_bounding_rectangle(region)
        for r, c in rectangle_coords:
            output_grid[r][c] = 4

    return output_grid