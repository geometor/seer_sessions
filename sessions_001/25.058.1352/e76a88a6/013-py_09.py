"""
1.  **Identify Gray Regions:** Find all contiguous regions of gray (5) pixels. A contiguous region is defined as a group of gray pixels that are directly adjacent (up, down, left, or right - not diagonal).

2.  **Alternating Color Replacement:** Within each identified gray region, replace the gray pixels with an alternating pattern of magenta (6) and azure (8). The alternation starts with magenta in the first column of the region. The next column within the region should have all gray pixels replaced with azure, etc.

3.  **Background Preservation:** Pixels that are not part of any gray region (in this case black (0)) remain unchanged.

4. **Contiguous rule:** in a contiguous block, columns alternate, rows do not.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to find contiguous pixels."""
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
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Find all contiguous regions of gray (5) pixels
    gray_regions = find_contiguous_regions(input_grid, 5)

    # Iterate through each gray region
    for region in gray_regions:
        # Determine the starting column index within the overall grid
        min_col = min(col for _, col in region)

        # Iterate through pixels in the region and apply alternating colors
        for row, col in region:
            # Alternate colors based on the column index
            if (col - min_col) % 2 == 0:
                output_grid[row, col] = 6  # Magenta
            else:
                output_grid[row, col] = 8  # Azure

    # Return the modified grid
    return output_grid