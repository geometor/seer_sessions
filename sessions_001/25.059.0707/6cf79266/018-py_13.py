"""
1.  **Identify White Regions:** Find all contiguous regions of white (0) pixels.
2.  **Check Region Height:** If the height of the white regions is less than 3, no changes are made.
3.  **Conditional Insertion, if applicable:** If a white region exists with a height of at least 3:
    *   Find the bottom-most row of the white region.
    *   Find the horizontal center column of the white region at the bottom row.
    *   Insert a 3x1 block of blue (1) pixels, with the top of the block at the identified bottom center location.
4. **Preserve Other Pixels:** Ensure all non-white pixels, especially the orange ones, remain unchanged.
"""

import numpy as np

def find_white_regions(grid):
    """Find contiguous white regions in the grid."""
    white_regions = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_region):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != 0
        ):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 0 and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                white_regions.append(current_region)
    return white_regions

def get_region_height(region):
    """Calculates the height of a region."""
    if not region:
        return 0
    rows = [r for r, _ in region]
    return max(rows) - min(rows) + 1

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    white_regions = find_white_regions(input_grid)

    # Iterate through white regions
    for region in white_regions:
        # Check region height
        height = get_region_height(region)
        if height >= 3:
            # Find bottom-most row
            bottom_row = max(region, key=lambda item: item[0])[0]

            # Find horizontal center at the bottom row
            region_cols_at_bottom = [col for row, col in region if row == bottom_row]
            insert_col = region_cols_at_bottom[len(region_cols_at_bottom) // 2]

            # Insert 3x1 blue block
            if bottom_row + 2 < output_grid.shape[0]:
                output_grid[bottom_row, insert_col] = 1
                output_grid[bottom_row + 1, insert_col] = 1
                output_grid[bottom_row + 2, insert_col] = 1
    return output_grid