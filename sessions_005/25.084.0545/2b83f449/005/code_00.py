"""
1.  **Identify Objects:**
    *   A **border object** consisting of connected pixels of colors 3 and 8.  This object forms a single-pixel-wide, continuous line around the edges and within the grid.
    *   An **irregular object** composed of pixels with color 7.
    *   The **background**, consisting of all pixels with color 0.

2.  **Border Transformation (Color Swap):**
    *   Within the *connected* border object, pixels of color 8 change to color 3, and pixels of color 3 change to color 8.

3.  **Irregular Object Transformation (Color Change):**
    *   All pixels of color 7 (the irregular object) change to color 6.

4.  **Adjacent Propagation:**
    *   Any pixel of color 8 that is *adjacent* (horizontally, vertically, or diagonally) to a pixel of color 6 changes to color 6. This propagation continues iteratively until no more color 8 pixels are adjacent to color 6 pixels.

5.  **Row Adjustment:**
    *  If the bottom row is all the same color, and it is different from the row above it, the entire row is deleted. The other rows shift down to fill the space, preserving all features.
"""

import numpy as np
from collections import deque

def get_adjacent_pixels(grid, row, col):
    # returns the adjacent pixels to (row, col) including diagonals, but NOT including (row, col)
    height, width = grid.shape
    adjacent_pixels = []
    for i in range(max(0, row - 1), min(height, row + 2)):
        for j in range(max(0, col - 1), min(width, col + 2)):
            if (i, j) != (row, col):
                adjacent_pixels.append((i, j))
    return adjacent_pixels

def flood_fill(grid, start_row, start_col, target_color, replacement_color):
    # Performs a flood fill, but only changes connected pixels.
    rows, cols = grid.shape
    if grid[start_row, start_col] != target_color:
        return
    q = deque([(start_row, start_col)])
    while q:
        row, col = q.popleft()
        if grid[row, col] == target_color:
            grid[row, col] = replacement_color
            for adj_row, adj_col in get_adjacent_pixels(grid, row, col):
                if 0 <= adj_row < rows and 0 <= adj_col < cols:
                    q.append((adj_row, adj_col))


def find_connected_border(grid):
    # Finds the connected border object of colors 3 and 8
    rows, cols = grid.shape
    border_pixels = set()
    visited = set()

    def dfs(row, col):
      # recursive depth first search to visit the boarder
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] not in (3, 8):
            return
        visited.add((row, col))
        border_pixels.add((row, col))
        for adj_row, adj_col in get_adjacent_pixels(grid, row, col):
            dfs(adj_row, adj_col)

    # Iterate through the grid's boundary to start DFS
    for r in range(rows):
        if grid[r, 0] in (3, 8):
            dfs(r, 0)
        if grid[r, cols - 1] in (3, 8):
            dfs(r, cols - 1)
    for c in range(1, cols - 1):  # Avoid corners (already checked)
        if grid[0, c] in (3, 8):
            dfs(0, c)
        if grid[rows - 1, c] in (3, 8):
            dfs(rows - 1, c)
    
    # now add internal pixels of color 3 and 8 that connect to the border
    visited = set()
    def dfs_internal(row,col):
      # recursive depth first search for connected internal pixels
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] not in (3, 8):
            return
        visited.add((row,col))
        # only add to border_pixels if connected to existing border
        is_connected = False
        for ar, ac in get_adjacent_pixels(grid,row,col):
            if (ar,ac) in border_pixels:
                is_connected = True
                break
        if is_connected:
            border_pixels.add((row,col))
            for ar, ac in get_adjacent_pixels(grid,row,col):
                dfs_internal(ar,ac)

    # add internal connected pixels
    for r in range(1, rows - 1):
      for c in range(1, cols - 1):
          dfs_internal(r,c)

    return border_pixels



def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify Objects (Border)
    border_pixels = find_connected_border(output_grid)

    # 2. Border Transformation (Color Swap)
    for row, col in border_pixels:
        if output_grid[row, col] == 3:
            output_grid[row, col] = 8
        elif output_grid[row, col] == 8:
            output_grid[row, col] = 3

    # 3. Irregular Object Transformation (Color Change)
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 7:
                output_grid[row, col] = 6

    # 4. Adjacent Propagation
    while True:
        changed = False
        new_grid = np.copy(output_grid)  # Create a copy for modifications
        for row in range(rows):
            for col in range(cols):
                if output_grid[row, col] == 8:
                    for adj_row, adj_col in get_adjacent_pixels(output_grid, row, col):
                        if 0 <= adj_row < rows and 0 <= adj_col < cols and output_grid[adj_row, adj_col] == 6:
                            new_grid[row, col] = 6  # Modify the copy
                            changed = True
                            break
        output_grid = new_grid  # Update output_grid
        if not changed:
            break

    # 5. Row Adjustment
    if rows > 1:  # Ensure there's a row above to compare with
      last_row = output_grid[-1]
      if np.all(last_row == last_row[0]) and not np.array_equal(last_row, output_grid[-2]):
          output_grid = output_grid[:-1,:]


    return output_grid