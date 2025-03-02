"""
1.  **Identify Blue Regions:** Find all distinct connected regions of blue (1) pixels in the input grid. Two blue pixels are connected if they are adjacent horizontally or vertically.
2.  **Classify and Recolor Blue Regions:**
    *   For each blue region:
        - Calculate the region's bounding box.
        - Count number of pixels inside the region.
        - **L-Shaped Regions:** A blue region considered "L-shaped" if the total number of blue pixels is strictly less than width*height of it's bounding box, and not a single pixel. Recolor these regions to orange (7).
        - **Rectangular Regions:** A blue region is considered "rectangular" if total number of blue pixels equals width*height of it's bounding box. Recolor to red (2).
        - **Other Regions:** Regions that do not meet the above condition remain blue.
3.  **Preserve Background:** All white (0) pixels in the input grid remain unchanged in the output grid.
"""

import numpy as np

def find_connected_regions(grid, color):
    """Finds connected regions of a specific color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to explore a connected region."""
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

        # Explore adjacent cells
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

def get_bounding_box(region):
    """Calculates the bounding box of a region."""
    min_row = min(r for r, _ in region)
    max_row = max(r for r, _ in region)
    min_col = min(c for _, c in region)
    max_col = max(c for _, c in region)
    return min_row, max_row, min_col, max_col

def is_l_shaped(region, grid):
    """Checks if a region is L-shaped (refined)."""
    if len(region) <= 1:  # Exclude single-pixel regions
        return False

    min_row, max_row, min_col, max_col = get_bounding_box(region)
    width = max_col - min_col + 1
    height = max_row - min_row + 1
    return len(region) < width * height

def is_rectangular(region, grid):
    """Checks if region is rectangular"""
    min_row, max_row, min_col, max_col = get_bounding_box(region)
    width = max_col - min_col + 1
    height = max_row - min_row + 1
    return len(region) == width * height


def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find connected regions of blue (color 1)
    blue_regions = find_connected_regions(input_grid, 1)

    # Recolor regions based on shape
    for region in blue_regions:
        if is_l_shaped(region, input_grid):
            # Recolor L-shaped regions to orange (7)
            for row, col in region:
                output_grid[row, col] = 7
        elif is_rectangular(region, input_grid):
            # Recolor rectangular regions to red
            for row, col in region:
                output_grid[row,col] = 2
        # else, keep the region blue.

    return output_grid