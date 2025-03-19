"""
1.  **Identify the Island:** Find the contiguous "island" of pixels containing blue, yellow, and azure colors. The island is defined by adjacent pixels (up, down, left, right - not diagonal).
2.  **Find the yellow:** find the yellow pixel in the island
3. **Add Blue:** add a blue pixel to the right of the yellow.
"""

import numpy as np

def find_island(grid, core_colors):
    """Finds the contiguous region of pixels with specified core colors."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    island_pixels = []

    # Find a starting pixel of a core color
    start_row, start_col = -1, -1
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in core_colors:
                start_row, start_col = r, c
                break
        if start_row != -1:
            break

    if start_row == -1:
        return []

    # Explore the connected region using DFS
    stack = [(start_row, start_col)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < rows and 0 <= c < cols and not visited[r, c]:
            visited[r, c] = True
            if grid[r, c] == 8 or grid[r,c] in core_colors :  # Include azure and core colors
                island_pixels.append((r, c))
                # Add neighbors to the stack
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    stack.append((r + dr, c + dc))

    return island_pixels

def find_yellow_pixel(grid, island_pixels):
    """Finds the yellow pixel within the island."""
    for r, c in island_pixels:
        if grid[r, c] == 4:  # Yellow
            return (r, c)
    return None


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the central "island"
    core_colors = [1, 4]  # Blue and Yellow
    island_pixels = find_island(input_grid, core_colors)

    if not island_pixels:
        return output_grid

    # 2. Find the yellow pixel
    yellow_pixel_coords = find_yellow_pixel(input_grid, island_pixels)

    if yellow_pixel_coords is None:
      return output_grid

    yellow_row, yellow_col = yellow_pixel_coords
    
    # 3. Add Blue to the right
    if yellow_col + 1 < cols:
          output_grid[yellow_row, yellow_col + 1] = 1

    return output_grid