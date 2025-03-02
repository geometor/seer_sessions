"""
1.  **Identify Grey Pixel Groups:** Find all groups of vertically connected grey (5) pixels within the input grid. Grey pixels in the same column that are directly adjacent are considered part of the same group.
2.  **Determine Transformation Color by Horizontal Position:**
    *   Order the identified grey pixel groups from left to right based on their column index.
    *   If a group is the first grey group from the left, change all its pixels to yellow (4).
    *   If a group is the second grey group, change all its pixels to red (2).
    *   If a group is the third or greater, change all its pixels to blue (1).
3.  **Apply Transformation:** Replace the grey (5) pixels in each identified vertical group with the `transformed_color` assigned in step 2.
4.  **Other Pixels:** All pixels that are not part of a grey vertical group remain unchanged.
"""

import numpy as np

def find_grey_pixel_groups(grid, color=5):
    """Finds groups of vertically connected grey pixels."""
    groups = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def dfs(row, col, current_group):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_group.append((row, col))
        # Check adjacent cells vertically
        dfs(row + 1, col, current_group)
        dfs(row - 1, col, current_group)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_group = []
                dfs(r, c, current_group)
                groups.append(current_group)
    return groups

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grey_groups = find_grey_pixel_groups(input_grid)

    # Sort groups by their horizontal position (column index of the first pixel)
    sorted_groups = sorted(grey_groups, key=lambda group: group[0][1])

    # Determine the output color for each group based on its position
    for i, group in enumerate(sorted_groups):
        if i == 0:  # First group
            output_color = 4  # Yellow
        elif i == 1:  # Second group
            output_color = 2  # Red
        else:  # Third or greater
            output_color = 1  # Blue

        # Apply the transformation
        for row, col in group:
            output_grid[row, col] = output_color

    return output_grid