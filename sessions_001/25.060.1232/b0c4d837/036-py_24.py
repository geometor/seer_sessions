"""
1.  **Identify the Enclosing Shape:** Find the contiguous region of gray (5) pixels that forms a recognizable shape (e.g., "U", "arch", "C").
2.  **Identify interior:** find the region within the gray shape.
3. **Output Interior:** Create a new grid consisting of the interior area.
"""

import numpy as np

def find_contiguous_region(grid, color_value):
    """Finds the coordinates of a contiguous region of a given color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    region = []

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color_value
        ):
            return
        visited[row, col] = True
        region.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color_value and not visited[row, col]:
                dfs(row, col)
                # Continue searching for other regions
                # return region # Do not return after just the first find
    return region


def get_neighbors(grid, row, col, include_diagonal=False):
    """
    Returns the valid neighbors of a pixel.
    """
    rows, cols = grid.shape
    neighbors = []
    
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))

    if include_diagonal:
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
              neighbors.append((new_row, new_col))
            
    return neighbors


def find_interior(grid, enclosing_color):
    """
    Finds the interior region enclosed by the given color.
    Assumes a single, fully enclosed region.
    """
    rows, cols = grid.shape
    enclosing_pixels = find_contiguous_region(grid, enclosing_color)
    
    # Find a starting point for the interior
    interior_start = None
    for r, c in enclosing_pixels:
      for nr, nc in get_neighbors(grid,r,c):
        if grid[nr,nc] != enclosing_color:
          interior_start = (nr, nc)
          break
      if interior_start:
        break
    if interior_start is None:
      return []

    # Flood fill from the starting point, avoiding the enclosing color
    visited = np.zeros_like(grid, dtype=bool)
    interior_pixels = []
    stack = [interior_start]

    while stack:
        row, col = stack.pop()
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] == enclosing_color):
            continue

        visited[row, col] = True
        interior_pixels.append((row, col))
        
        for nr,nc in get_neighbors(grid, row, col, include_diagonal=True):
          stack.append((nr,nc))


    return interior_pixels

def transform(input_grid):
    # Find the contiguous region of gray (5) pixels.
    enclosing_color = 5
    interior_pixels = find_interior(input_grid, enclosing_color)

    # Create a bounding box for the interior pixels
    if interior_pixels:
      min_row = min(r for r, _ in interior_pixels)
      max_row = max(r for r, _ in interior_pixels)
      min_col = min(c for _, c in interior_pixels)
      max_col = max(c for _, c in interior_pixels)

      # Create output grid
      output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

      for r, c in interior_pixels:
        output_grid[r-min_row, c-min_col] = input_grid[r,c]

    else:
        output_grid = np.zeros_like(input_grid, dtype=int)

    return output_grid