"""
The transformation replaces 0s (white pixels) in the input grid with 2s, 3s, or 4s based on their proximity and direction relative to 5s (gray pixels).  The replacement appears to follow a clockwise pattern *from* the 5.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
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

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def get_replacement_color(five_pos, zero_pos):
    """Determines the replacement color for a zero based on its position relative to a five."""
    five_row, five_col = five_pos
    zero_row, zero_col = zero_pos

    # Calculate relative position
    row_diff = zero_row - five_row
    col_diff = zero_col - five_col
    
    if row_diff == 0 and col_diff > 0:
        return 3  # Right of five
    elif row_diff < 0 and col_diff ==0:
        return 3
    elif row_diff < 0 and col_diff > 0:
        return 3
    elif row_diff > 0 and col_diff == 0:
        return 2  # Below five
    elif row_diff > 0 and col_diff > 0:
        return 2
    elif row_diff > 0 and col_diff < 0:
        return 2
    elif row_diff == 0 and col_diff < 0:
        return 4  # Left of five
    elif row_diff < 0 and col_diff < 0:
        return 4
    elif row_diff < 0 and col_diff == 0:
        return 3

    return 4 # default should never be reached
        


def transform(input_grid):
    # Initialize output_grid with a copy of the input grid
    output_grid = input_grid.copy()

    # Find contiguous regions of 0s and 5s
    zero_regions = find_contiguous_regions(input_grid, 0)
    five_regions = find_contiguous_regions(input_grid, 5)

    # Iterate through each zero region
    for zero_region in zero_regions:
        # Find the nearest five region (simplified for this task: just use the first five)
        if five_regions:  # Check if five_regions is not empty
            # Use the first five found for replacement logic
            
            for five_region in five_regions:
              for five_pos in five_region:
                for zero_pos in zero_region:
                    replacement_color = get_replacement_color(five_pos, zero_pos)
                    output_grid[zero_pos] = replacement_color

    return output_grid