"""
The transformation replaces regions of gray (5) pixels in the input grid with a checkerboard pattern of magenta (6) and azure (8) pixels. The checkerboard pattern starts with magenta in the top-left corner of each gray region.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """
    Finds all contiguous regions of a given color in a grid.
    Returns a list of sets, where each set contains the (row, col) coordinates of a contiguous region.
    """
    rows, cols = grid.shape
    visited = set()
    regions = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_region):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_region.add((r, c))

        # Explore adjacent cells (up, down, left, right)
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_region = set()
                dfs(r, c, current_region)
                regions.append(current_region)

    return regions

def transform(input_grid):
    """
    Transforms the input grid by replacing gray areas with a magenta/azure checkerboard.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all contiguous regions of gray pixels
    gray_regions = find_contiguous_regions(input_grid, 5)

    # Replace each gray region with a checkerboard pattern
    for region in gray_regions:
        # Find the top-left corner of the region
        min_row = min(r for r, _ in region)
        min_col = min(c for _, c in region)

        # Apply checkerboard pattern
        for r, c in region:
            # Determine if the cell should be magenta or azure
            if (r - min_row + c - min_col) % 2 == 0:
                output_grid[r, c] = 6  # Magenta
            else:
                output_grid[r, c] = 8  # Azure

    return output_grid