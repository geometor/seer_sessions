"""
1. Identify Regions: Find all contiguous regions of white pixels (color 0) in the input grid.
2. Remove Regions: Completely eliminate all identified contiguous regions of white pixels.
3. Preserve Non-White: Keep all remaining non-white pixels.
4. Collapse output: The output dimensions match the bounding box of the preserved non-white pixels.
5. Construct Output: Create a new grid containing *only* the preserved non-white pixels, adjusting the grid dimensions to fit tightly around these remaining pixels. The output is a collapsed version of the preserved non-white pixels.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """
    Finds contiguous regions of a specific color in the grid.

    Args:
        grid: The input grid (2D numpy array).
        color: The color to search for.

    Returns:
        A list of sets, where each set contains the (row, col) coordinates of a contiguous region.
    """
    visited = set()
    regions = []

    def dfs(row, col, current_region):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_region.add((row, col))
        # Check neighbors (up, down, left, right)
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_region = set()
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    """
    Transforms the input grid by removing all white regions and collapsing the output.
    """
    grid = np.array(input_grid)

    # Find all non-white pixel coordinates
    non_white_coords = [(r, c) for r in range(grid.shape[0]) for c in range(grid.shape[1]) if grid[r, c] != 0]

    # If there are no non-white pixels, return an empty grid
    if not non_white_coords:
        return []

    # Find the bounding box of the non-white pixels
    min_row, min_col = np.min(non_white_coords, axis=0)
    max_row, max_col = np.max(non_white_coords, axis=0)

    # Create the output grid
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the non-white pixels to the output grid
    for r, c in non_white_coords:
        output_grid[r - min_row, c - min_col] = grid[r, c]

    return output_grid.tolist()