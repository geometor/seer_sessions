"""
The transformation identifies colored regions (contiguous blocks of non-white pixels, including single pixels) within the input grid. 
For each colored region, it duplicates the region and appends it immediately to the right of the original region.
The number of pixels added to the right is equal to the original width of the region.
"""

import numpy as np

def find_colored_regions(grid):
    """
    Finds all contiguous colored regions (including single pixels).
    Returns a list of regions, where each region is a list of (row, col, color) tuples.
    """
    rows, cols = grid.shape
    regions = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_region):
        visited.add((r, c))
        current_region.append((r, c, grid[r, c]))

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if is_valid(nr, nc) and (nr, nc) not in visited and grid[nr, nc] == grid[r, c]:
                dfs(nr, nc, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)

    return regions

def transform(input_grid):
    """
    Transforms the input grid by identifying colored regions and extending them to the right.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find colored regions
    regions = find_colored_regions(input_grid)
    
    # Iterate through each region
    for region in regions:
        # Determine the width of the region
        min_col = min(pixel[1] for pixel in region)
        max_col = max(pixel[1] for pixel in region)
        width = max_col - min_col + 1

        # Extend the region to the right
        for r, c, color in region:
            for i in range(width):
                new_col = c + width + i  # Calculate new column index
                if new_col < cols: # make sure not outside grid
                    output_grid[r, new_col] = color

    return output_grid