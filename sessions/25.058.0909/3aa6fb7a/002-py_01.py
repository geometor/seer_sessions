"""
1.  **Identify Objects:** Find all groups of contiguous azure (8) pixels within the input grid.
2.  **Identify border pixels.** For each group of azure (8) pixels identify border pixels
3.  **Locate Target Pixels:** Find the specific azure pixels that are along the border of the group with white background.
4.  **Transform:** Change the color of one of these border azure (8) pixels in each group to blue (1).
5.  **Output:** Create a new grid with the modified pixel colors, leaving all other pixels unchanged.
"""

import numpy as np

def find_pixel_groups(grid, color):
    """Finds groups of contiguous pixels of a given color."""
    visited = np.zeros_like(grid, dtype=bool)
    groups = []

    def dfs(row, col, current_group):
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
        current_group.append((row, col))
        dfs(row + 1, col, current_group)
        dfs(row - 1, col, current_group)
        dfs(row, col + 1, current_group)
        dfs(row, col - 1, current_group)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                current_group = []
                dfs(row, col, current_group)
                groups.append(current_group)
    return groups

def find_border_pixels(grid, group):
    """Finds border pixels of a group that touch white (0) pixels."""
    border_pixels = []
    for row, col in group:
        neighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]
        for n_row, n_col in neighbors:
            if (
                0 <= n_row < grid.shape[0]
                and 0 <= n_col < grid.shape[1]
                and grid[n_row, n_col] == 0
            ):
                border_pixels.append((row, col))
                break  # Move to the next pixel in the group
    return border_pixels

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find all groups of contiguous azure (8) pixels
    azure_groups = find_pixel_groups(input_grid, 8)
    
    # Iterate through each azure group
    for group in azure_groups:
        # Find border pixels that touch white (0) pixels
        border_pixels = find_border_pixels(input_grid, group)
        
        #if border pixels are found, pick the first and change the color
        if(border_pixels):
            target_pixel = border_pixels[0]
            output_grid[target_pixel] = 1

    # Return the modified grid
    return output_grid