"""
1.  **Divide:** Split the input grid vertically into two halves (top and bottom).
2.  **Top Half Fill:** In the top half, identify all red pixels. Expand this red region to fill any *completely enclosed* blue pixels. "Enclosed" means surrounded by red or the edge of the top half grid in all directions (up, down, left, right, and diagonals).
3.  **Bottom Half Clear:**  In the bottom half, remove all red pixels.
4.  **Copy and Shift:** Copy the filled red region from the top half.
5.  **Paste to Bottom.** Paste this copy into the bottom half of the *output* grid using a consistent vertical offset based on original red pixel locations. The exact offset is determined by the number of rows between top red and bottom red.
"""

import numpy as np
from collections import deque

def get_neighbors(grid, row, col):
    """Gets the 8 neighbors of a cell (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def fill_enclosed(grid, start_color=1, fill_color=2):
    """Fills enclosed regions of start_color with fill_color."""
    rows, cols = grid.shape
    visited = set()
    
    # Find all pixels of start_color to potentially start filling from
    start_pixels = []
    for r in range(rows):
        for c in range(cols):
          if grid[r,c] == start_color:
            start_pixels.append((r,c))

    for start_row, start_col in start_pixels:
        if (start_row, start_col) in visited:
            continue

        q = deque([(start_row, start_col)])
        region = []
        enclosed = True

        while q:
            row, col = q.popleft()

            if (row, col) in visited:
                continue
            visited.add((row, col))

            if grid[row, col] == start_color:
                region.append((row, col))
                neighbors = get_neighbors(grid, row, col)
                for nr, nc in neighbors:
                    if not (0 <= nr < rows and 0 <= nc < cols): # Check the boundary
                        enclosed = False
                    elif grid[nr, nc] != start_color and grid[nr, nc] != fill_color: #check that the neighbor is one of the two colors
                        enclosed = False
                    elif (nr, nc) not in visited:
                        q.append((nr, nc))

        if enclosed:
            for row, col in region:
                grid[row, col] = fill_color

    return grid

def get_top_red(input_grid, mid_row):
    top_red_pixels = []
    rows, cols = input_grid.shape
    for r in range(0, mid_row):
        for c in range(cols):
            if input_grid[r, c] == 2:
                top_red_pixels.append((r, c))
    return top_red_pixels

def get_bottom_red_row(input_grid):
  rows, _ = input_grid.shape
  for r in range(rows-1, -1, -1): # efficient search from bottom
      for c in range(input_grid.shape[1]):
          if input_grid[r,c] == 2:
              return r
  return -1

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    mid_row = rows // 2

    # 1. Divide (Implicit in the loop ranges)

    # 2. Top Half Fill
    top_half = output_grid[:mid_row, :]
    fill_enclosed(top_half)
    output_grid[:mid_row, :] = top_half
    
    # find the lowest row of top red
    top_red_pixels = get_top_red(output_grid, mid_row)
    if len(top_red_pixels) > 0:
        top_red_row = max(r for r, _ in top_red_pixels)
    else:
      top_red_row = -1

    # 3. Bottom Half Clear
    output_grid[mid_row:, :] = np.where(output_grid[mid_row:, :] == 2, 0, output_grid[mid_row:, :])

    # Find offset
    bottom_red_row = get_bottom_red_row(input_grid)

    # 4. Copy and Shift & 5. Paste to Bottom.
    if top_red_row != -1 and bottom_red_row != -1:
      row_offset = bottom_red_row - top_red_row
      
      for r,c in top_red_pixels:
          new_r = r + row_offset
          if 0 <= new_r < rows:
              output_grid[new_r,c] = 2

    return output_grid