"""
1.  **Identify Target Shape:** Examine the input grid and identify if there is a rectangle of uniform color other than gray (5).
2.  **Prioritize Non-Gray Rectangles:**
    *   If a non-gray rectangle exists: Extract the rectangular region of that color to create the output grid.
    *   If No non-gray rectangle exists: Find the gray (5) shape that encloses other colored pixels. Extract the area enclosed by this gray region.
3.  **Output:** The output grid contains *only* the extracted shape from step 2.
"""

import numpy as np
from collections import Counter

def find_contiguous_regions(grid):
    """Finds all contiguous regions of all colors."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = {}

    def dfs(row, col, color, region):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        region.append((row, col))
        dfs(row + 1, col, color, region)
        dfs(row - 1, col, color, region)
        dfs(row, col + 1, color, region)
        dfs(row, col - 1, color, region)

    for row in range(rows):
        for col in range(cols):
            color = grid[row, col]
            if not visited[row, col]:
                region = []
                dfs(row, col, color, region)
                if color not in regions:
                    regions[color] = []
                regions[color].append(region)
    return regions

def calculate_region_extents(region):
    """Calculate the bounding box (min_row, min_col, max_row, max_col) for a region."""
    if not region:
        return None  # Handle empty regions
    min_row = min(r for r, _ in region)
    min_col = min(c for _, c in region)
    max_row = max(r for r, _ in region)
    max_col = max(c for _, c in region)
    return (min_row, min_col, max_row, max_col)

def is_rectangle(region, grid):
   """check if region consists of connected cells forming a rectangle"""
   min_row, min_col, max_row, max_col = calculate_region_extents(region)
   color = grid[region[0][0], region[0][1]]

   for r in range(min_row, max_row + 1):
       for c in range(min_col, max_col + 1):
          if (r,c) not in region:
            return False
          if grid[r,c] != color:
            return False

   return True

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

def find_contiguous_region(grid, color_value):
  """Finds one contiguous region"""
  regions = find_contiguous_regions(grid)
  if color_value in regions:
    return regions[color_value][0]
  return []
  

def transform(input_grid):
    # Find all contiguous regions
    regions = find_contiguous_regions(input_grid)

    # Check for non-gray rectangles
    target_region = None
    target_color = None
    for color, region_list in regions.items():
        if color != 5:  # Not gray
            for region in region_list:
                if is_rectangle(region, input_grid):
                    target_region = region
                    target_color = color
                    break  # Prioritize the *first* non-gray rectangle found
        if target_region:
            break

    # If no non-gray rectangle, find the interior of gray
    if target_region is None:
      interior_pixels = find_interior(input_grid, 5)
      if interior_pixels:
        target_region = interior_pixels


    # Create output grid based on target_region
    if target_region:
        min_row, min_col, max_row, max_col = calculate_region_extents(target_region)
        output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

        #fill output grid
        for r, c in target_region:
          if target_color is not None:
            output_grid[r - min_row, c - min_col] = target_color
          else:
            output_grid[r - min_row, c - min_col] = input_grid[r,c]

    else: # Handle cases with no identified region
        output_grid = np.empty((0,0), dtype=int)

    return output_grid