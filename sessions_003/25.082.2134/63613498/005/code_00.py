"""
Transforms an input grid by changing the color of pixels based on their adjacency to gray (5) pixels.

1. Identify Pixel Groups: Divide the input grid into connected groups of pixels.
   A "connected group" is a set of pixels of the same color where each pixel is
   directly adjacent (horizontally, vertically, or diagonally) to at least one
   other pixel in the group. Exclude white pixels (color 0).
2. Check for Gray Adjacency: For each identified pixel group, determine if *any*
   of its pixels are adjacent (horizontally, vertically, or diagonally) to a gray
   pixel (color 5).
3. Apply Color Change Rules:
    * If a pixel group has the color 9 (maroon), change all pixels in that group to 5 (gray).
    * If a pixel group has a color in the set [1 (blue), 3 (green), 4 (yellow), 6 (magenta), 7 (orange), 8 (azure)],
      and *none* of the pixels in that group are adjacent to a gray pixel, change all pixels in that group to 5 (gray).
    * Otherwise, the pixel group's color remains unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the coordinates of all 8 neighbors of a pixel."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the pixel itself
                neighbors.append((i, j))
    return neighbors

def is_adjacent_to_gray(grid, pixel_group):
    """Checks if any pixel in the group is adjacent to a gray pixel."""
    for row, col in pixel_group["locations"]:
        neighbors = get_neighbors(grid, row, col)
        for n_row, n_col in neighbors:
            if grid[n_row, n_col] == 5:
                return True
    return False

def identify_pixel_groups(grid):
    """Identifies connected groups of pixels with the same non-white color."""
    rows, cols = grid.shape
    visited = set()
    pixel_groups = []

    def dfs(row, col, color, current_group):
        """Depth-first search to find connected pixels."""
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_group.append((row, col))
        for n_row, n_col in get_neighbors(grid, row, col):
            dfs(n_row, n_col, color, current_group)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_group = []
                dfs(r, c, grid[r, c], current_group)
                pixel_groups.append({"color": grid[r, c], "locations": current_group})
    return pixel_groups

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    pixel_groups = identify_pixel_groups(input_grid)

    for group in pixel_groups:
        # Apply rule for color 9
        if group["color"] == 9:
            for r, c in group["locations"]:
                output_grid[r, c] = 5
        # Apply rule for colors 1, 3, 4, 6, 7, and 8
        elif group["color"] in [1, 3, 4, 6, 7, 8]:
            if not is_adjacent_to_gray(input_grid, group):
                for r, c in group["locations"]:
                    output_grid[r, c] = 5

    return output_grid