"""
1.  **Identify White Regions:** Find all contiguous regions of white pixels (color 0) in the input grid.

2.  **For Each White Region:**
    *   Determine the bottom-most row of the white region.
    *   Calculate the insertion column as the horizontal center of the bottom row of the white region.
    *   Calculate available space - Determine the number of rows available below the bottom-most row, up to the bottom edge of the grid.
    *   Insert Blue Block:
        *   If the available space is 1 or more, insert a column of blue pixels (color 1) starting at the bottom row and extending downwards. The height of this column is equal to the minimum of the `available_space` and 3. If there isn't enough space for even one pixel, no change.
        * example: if space is 1, insert 1 pixel.
        * example: if space is 2, insert 2 pixel.
        * example: if space is 3 or greater, insert 3 pixels.
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

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    white_regions = find_white_regions(input_grid)

    # Iterate through identified white regions
    for region in white_regions:
        #find bottom row for region
        if len(region) > 0:

          bottom_row = max(region, key=lambda item: item[0])[0]
          region_cols = [col for row, col in region if row == bottom_row]

          #insert at the bottom, center of each region.
          if len(region_cols) > 0:
            insert_col = region_cols[len(region_cols) // 2]

            # Calculate available space
            available_space = output_grid.shape[0] - 1 - bottom_row

            # Insert Blue Block
            block_height = min(available_space, 3)
            for i in range(block_height):
                output_grid[bottom_row + i, insert_col] = 1

    return output_grid