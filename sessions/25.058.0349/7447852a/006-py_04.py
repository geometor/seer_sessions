"""
1.  **Identify Red Pixels:** Scan the input grid to locate all red pixels (color value 2).
2.  **Classify Red Pixels:**
    *   **Isolated:** A red pixel is *isolated* if it has no adjacent red pixels (horizontally or vertically).
    *  **Small Region**: collection of 2 pixels
    *   **Large Region Member:** A red pixel is a *region member* if it's part of a contiguous group of 3 or more red pixels, connected horizontally or vertically.
3.  **Transform Large Regions:** Change the color of red pixels that are *large region members* to yellow (color value 4).
4. **Preserve Other Pixels**: All other colors and isolated/small region red pixels should maintain their original colors.
"""

import numpy as np

def find_regions(grid, color):
    """Finds contiguous regions of a given color in the grid."""
    visited = set()
    regions = []

    def is_valid(x, y):
        """Checks if a coordinate is within the grid bounds."""
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_region):
        """Performs Depth-First Search to explore a region."""
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != color:
            return
        visited.add((x, y))
        current_region.append((x, y))

        # Explore adjacent cells (up, down, left, right)
        dfs(x + 1, y, current_region)
        dfs(x - 1, y, current_region)
        dfs(x, y + 1, current_region)
        dfs(x, y - 1, current_region)


    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if (x, y) not in visited and grid[x, y] == color:
                current_region = []
                dfs(x, y, current_region)
                regions.append(current_region) # Append all regions found

    return regions

def transform(input_grid):
    """Transforms red regions of size 3 or more to yellow."""
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all red regions
    red_regions = find_regions(input_grid, 2)

    # Transform large regions (size >= 3) to yellow
    for region in red_regions:
        if len(region) >= 3:
            for x, y in region:
                output_grid[x, y] = 4

    return output_grid