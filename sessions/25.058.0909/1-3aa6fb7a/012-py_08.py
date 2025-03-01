"""
Identifies contiguous regions of azure (8) pixels in the input grid.
Then, changes a subset of these azure pixels to blue (1) based on a line-tracing rule.
The rule traces the outer perimeter of each azure region, changing azure pixels to blue
if they are part of the outer "edge" of the shape, considering both the top/left edges
and pixels adjacent to internal empty spaces.
The original grid dimensions and the positions of unchanged pixels are preserved.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """
    Finds contiguous regions (objects) of a specific color in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                regions.append(dfs(row, col))

    return regions

def get_perimeter(grid, region):
    """
    Gets the perimeter of a region, considering top/left edges and internal gaps.
    """
    perimeter = []
    for row, col in region:
        # Check if it's on the top or left edge of the entire grid
        if row == 0 or col == 0:
            perimeter.append((row, col))
            continue

        # Check neighbors
        is_perimeter = False
        if grid[row - 1, col] != 8:  # Check above
            is_perimeter = True
        if grid[row, col - 1] != 8:  # Check left
            is_perimeter = True

        if is_perimeter:
            perimeter.append((row, col))

    return perimeter

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    # Find azure regions
    azure_regions = find_contiguous_regions(input_grid, 8)

    # change output pixels 
    for region in azure_regions:
        # Get the refined perimeter
        perimeter_pixels = get_perimeter(input_grid, region)
        # Change perimeter color to blue
        for row, col in perimeter_pixels:
            output_grid[row, col] = 1

    return output_grid