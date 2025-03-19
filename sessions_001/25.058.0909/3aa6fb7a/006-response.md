# 1-3aa6fb7a • 006 • refine_coder

---
```python
"""
1.  **Identify Azure Regions:** Find all distinct, contiguous groups of azure (8) pixels in the input grid.  Contiguous means connected horizontally or vertically (not diagonally).
2.  **Identify Border Pixels:** Within each azure region, identify the border pixels. A border pixel is an azure (8) pixel directly adjacent (horizontally or vertically) to at least one white (0) pixel.
3.  **Locate target pixel:** Find what could be called a "corner" of the azure object. A corner pixel is identified as any azure border pixel adjacent to at least two white pixels, *but also* including the pixels above and to the left of the current pixel.
4.  **Select Target Pixel**: Among these 'corner' pixels, locate the one that is the top-left most.
5.  **Transform:** Change the color of the identified top-left corner pixel to blue (1).
6.  **Output:** Create a new grid identical to the input, except for the pixel transformed in the previous step.
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

def find_corner_pixels(grid, border_pixels):
    """Finds corner pixels among border pixels."""
    corner_pixels = []
    for row, col in border_pixels:
        white_neighbors = 0
        neighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
            (row -1, col -1) # Include top-left neighbor
        ]
        for n_row, n_col in neighbors:
            if (
                0 <= n_row < grid.shape[0]
                and 0 <= n_col < grid.shape[1]
                and grid[n_row, n_col] == 0
            ):
                white_neighbors += 1
        if white_neighbors >= 2:
            corner_pixels.append((row, col))
    return corner_pixels

def find_top_leftmost_pixel(pixels):
    """Finds the top-leftmost pixel from a list of pixels."""
    if not pixels:
        return None
    min_row = min(pixel[0] for pixel in pixels)
    min_col = min(pixel[1] for pixel in pixels if pixel[0] == min_row)
    return (min_row, min_col)

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find all groups of contiguous azure (8) pixels
    azure_groups = find_pixel_groups(input_grid, 8)

    # Iterate through each azure group
    for group in azure_groups:
        # Find border pixels that touch white (0) pixels
        border_pixels = find_border_pixels(input_grid, group)
        
        # Find corner pixels
        corner_pixels = find_corner_pixels(input_grid, border_pixels)

        # Find the top-leftmost corner pixel
        target_pixel = find_top_leftmost_pixel(corner_pixels)

        # Change the color of the target pixel to blue (1)
        if target_pixel:
            output_grid[target_pixel] = 1

    # Return the modified grid
    return output_grid
```
