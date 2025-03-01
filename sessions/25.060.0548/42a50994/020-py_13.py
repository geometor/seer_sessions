"""
1.  **Identify Gray Regions:** Find all connected regions of gray (5) pixels. A region is defined as one or more gray pixels that are directly adjacent to each other (horizontally or vertically, but *not* diagonally).
2.  **Process Each Region:** For each identified gray region:
    *   Find the leftmost pixel within the region (the pixel with the minimum column index).
    *   Change all gray pixels in the region to white (0), *except* for the leftmost pixel identified in the previous step.  The leftmost pixel retains its original gray color.
"""

import numpy as np

def find_gray_regions(grid):
    """Finds all connected regions of gray pixels in the grid."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    regions = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_region):
        """Depth-first search to find connected components."""
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != 5:
            return
        visited.add((r, c))
        current_region.append((r, c))

        # Explore adjacent cells (up, down, left, right)
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 5 and (r, c) not in visited:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    """Transforms the input grid by modifying gray regions."""
    output_grid = np.copy(input_grid)
    gray_regions = find_gray_regions(input_grid)

    for region in gray_regions:
        # Find the western-most edge (minimum column index) within the region
        min_col = min(cell[1] for cell in region)

        # Process each pixel in the region
        for r, c in region:
            if c > min_col:  # Not the western-most edge within the region
                output_grid[r][c] = 0

    return output_grid