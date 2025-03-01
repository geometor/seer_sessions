"""
The program identifies all of the disconnected regions of grey, and replaces the a 2x2 area inside with another solid color. each region has different color. the selection criteria for which 2x2 region to replace, and the color used for replacement appears arbitrary, but is consistent across each distinct example, suggesting that it could be predicted.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds all contiguous regions of a specific color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to explore a contiguous region."""
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

def find_2x2_subregion(region):
    """
    Finds a 2x2 subregion within a larger region, prioritizing top-left corners.
    Returns the top-left coordinate of a 2x2 square if found, otherwise None.

    Brute Force Method:
        The simplest way to find a 2 x 2 subregion is a brute force search
        for each pixel, check if a 2x2 block can be formed below to the right
    """
    region_set = set(region)
    for row, col in region:
            if (row + 1, col) in region_set and \
               (row, col + 1) in region_set and \
               (row + 1, col + 1) in region_set:
                return (row,col)

    return None


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    # Find all contiguous gray regions.
    gray_regions = find_contiguous_regions(input_grid, 5)

    # color map for replacement
    color_map = {
        0: 8,  # First region gets color 8 (azure)
        1: 7,  # Second region gets color 7 (orange)
        2: 6   # Third region gets color 6 (magenta)
    }

    # Iterate through the gray regions and replace subregions.
    for i, region in enumerate(gray_regions):
       # find a 2x2 sub region
        subregion_start = find_2x2_subregion(region)

        if subregion_start:
          # select a color for this region
          fill_color = color_map.get(i,6) # default if more regions
          # replace those pixels in this square area with the new color
          row, col = subregion_start
          output_grid[row, col] = fill_color
          output_grid[row + 1, col] = fill_color
          output_grid[row, col + 1] = fill_color
          output_grid[row + 1, col + 1] = fill_color

    return output_grid