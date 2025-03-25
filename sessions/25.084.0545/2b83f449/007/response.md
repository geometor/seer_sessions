```python
"""
1.  **Identify Objects:**
    *   A **connected_border** object: A single-pixel-wide, continuous line of pixels of colors 3 and 8, forming a boundary around and potentially inside the grid. "Continuous" means each pixel in the border is adjacent (horizontally, vertically, or diagonally) to at least one other pixel in the border, forming a closed loop or loops.
    *   An **irregular_object**: One or more pixels of color 7 inside the region(s) defined by the connected_border.
    *   **Background:** All pixels with color 0.

2.  **Border Color Swap:**
    *   Within the *connected_border* object, swap colors: 3 becomes 8, and 8 becomes 3.

3.  **Irregular Object Color Change:**
    *   Change all pixels of color 7 to color 6.

4.  **Bounded Propagation:**
    *   Within the area enclosed by the `connected_border`, any pixel of color 8 that is *adjacent* (horizontally, vertically, or diagonally) to a pixel of color 6 changes to color 6. This propagation happens iteratively until no more color 8 pixels adjacent to color 6 pixels within the border are found.

5. **Row Adjustment**:

    *  Check if all pixels in the last row of the grid have the same color.
    *  If they do, check if that color is different from the color of all pixels in the row above it.
    * If both conditions are true, delete the last row and allow the remaining rows to shift down.
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

def find_connected_border(grid):
    # Finds the connected border object of colors 3 and 8.
    rows, cols = grid.shape
    border_pixels = set()
    visited = set()

    def dfs(row, col):
        # Recursive depth-first search to identify connected border pixels.
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] not in (3, 8):
            return
        visited.add((row, col))
        border_pixels.add((row, col))

        # Explore adjacent cells.
        for adj_row, adj_col in get_adjacent_pixels(grid, row, col):
            dfs(adj_row, adj_col)

    # Start DFS from the outer boundary.  This will find the *outer* border.
    for r in range(rows):
        dfs(r, 0)  # Left edge
        dfs(r, cols - 1)  # Right edge
    for c in range(1, cols - 1):
        dfs(0, c)  # Top edge
        dfs(rows - 1, c)  # Bottom edge

    # Now find internal borders by checking 3 and 8 pixels connected to existing borders
    
    internal_visited = set()
    def dfs_internal(row, col):
      # recursive depth first search for connected internal pixels
        if (row, col) in internal_visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] not in (3, 8):
            return
        internal_visited.add((row,col))
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

def bounded_flood_fill(grid, start_row, start_col, border_pixels):
    # Performs a flood fill of 8's to 6's, but *only* within the border,
    # starting from seeds of 6's (originally 7's)
    rows, cols = grid.shape
    if grid[start_row, start_col] != 6:
        return

    q = deque([(start_row, start_col)])
    visited = set() # avoid infinite loops
    visited.add((start_row,start_col))

    while q:
        row, col = q.popleft()
        # find neighbors that are 8 and inside border
        for adj_row, adj_col in get_adjacent_pixels(grid, row, col):
            if (adj_row,adj_col) not in visited:
                if (0 <= adj_row < rows and 0 <= adj_col < cols and
                        grid[adj_row, adj_col] == 8 and (adj_row,adj_col) not in border_pixels
                   ):
                    # if neighbor is an 8, is *inside* the border (not ON border)
                    # convert to a 6, and add to queue
                    grid[adj_row, adj_col] = 6
                    q.append((adj_row, adj_col))
                    visited.add((adj_row,adj_col))



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

    # 4. Bounded Propagation.
    # Iterate and find starting points for flood fill
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 6:
                bounded_flood_fill(output_grid, r, c, border_pixels)

    # 5. Row Adjustment
    if rows > 1: # make sure there is a row to delete
      last_row = output_grid[-1, :]
      if np.all(last_row == last_row[0]):  # Check if the last row is all the same color
          second_last_row = output_grid[-2, :]
          if not np.array_equal(last_row, second_last_row):  # Compare with the row above
              output_grid = output_grid[:-1, :]  # Delete the last row

    return output_grid
```