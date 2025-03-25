"""
1.  **Identify Blue Regions:** Find all connected regions of blue pixels in the input grid. A connected region is defined as a group of blue pixels where each pixel is directly adjacent (up, down, left, or right) to at least one other pixel in the region.
2.  **Find Left and Right Boundaries:** For each blue region, determine its leftmost and rightmost column boundaries, and its top and bottom row boundaries.
3.  **Iterate from Top to Bottom:** Starting from the top row of the grid and processing through to the bottom row
4.  **Place Red Pixels based on Left Boundary**: Within each row:
    *   Iterate through columns starting one position to the left of the leftmost blue pixel, and proceed leftwards
    *   Stop if a blue pixel is encountered
    *   If the current cell is not blue, change color to red
"""

import numpy as np

def find_blue_regions(grid):
    """Finds connected regions of blue pixels (value 1)."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    blue_regions = []

    def dfs(r, c, current_region):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != 1):
            return
        visited[r, c] = True
        current_region.append((r, c))
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1 and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                blue_regions.append(current_region)
    return blue_regions

def get_region_boundaries(region):
    """Calculates the leftmost and rightmost columns, and top and bottom rows of a region."""
    if not region:
        return None, None, None, None
    rows, cols = zip(*region)
    leftmost_column = min(cols)
    rightmost_column = max(cols)
    top_row = min(rows)
    bottom_row = max(rows)
    return leftmost_column, rightmost_column, top_row, bottom_row

def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.copy(grid)

    # Find blue regions
    blue_regions = find_blue_regions(grid)

    # find global left boundary
    leftmost_blue_column = cols # default to grid width
    for region in blue_regions:
      leftmost_column, _, _, _ = get_region_boundaries(region)
      leftmost_blue_column = min(leftmost_column, leftmost_column)

    # Iterate from Top to Bottom
    for row in range(rows):
        # Place Red Pixels based on Left Boundary
        for col in range(leftmost_blue_column -1 , -1, -1):  # Iterate leftwards
            if output_grid[row, col] == 1:
                break  # Stop if blue is encountered
            output_grid[row, col] = 2  # Change to red

    return output_grid.tolist()