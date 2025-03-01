"""
1.  **Identify Anchors:** Locate all grey (5) cells. These generally remain in their original positions.

2.  **Propagate Left to Right**.  Consider each non-grey and non-white cell, moving it along the row as follows:
    *   Iterate through all non-grey and non-white cells in reading order (left to right, top to bottom)
    *  If a non-grey, non-white pixel has a grey (5) pixel anywhere above it in the same column, move it to first empty cell on the same column, directly above the nearest grey (5).
    *   If a non-grey, non-white pixel has a grey (5) pixel anywhere below it in the same column, move it to first empty cell on the same column, directly below the nearest grey (5).
    *   When a pixel is moved on row to above a gray, check the right adjacent pixel of its orginal position and if not 0, move the value to above the neighboring grey as well.

3. Copy any not moved non-grey and non-white to the output.
"""

import numpy as np

def find_nearest_grey_above(grid, row, col):
    """Finds the nearest grey (5) cell above the given cell in the same column."""
    for r in range(row - 1, -1, -1):
        if grid[r][col] == 5:
            return r
    return -1

def find_nearest_grey_below(grid, row, col):
    """Finds the nearest grey (5) cell below the given cell in the same column."""
    for r in range(row + 1, len(grid)):
        if grid[r][col] == 5:
            return r
    return -1

def find_first_empty_above(grid, row, col):
    """Finds the first empty (0) cell above the given row in the same column."""
    for r in range(row - 1, -1, -1):
        if grid[r][col] == 0:
            return r
    return -1

def find_first_empty_below(grid, row, col):
    """Finds the first empty (0) cell below the given row in the same column."""
    for r in range(row + 1, len(grid)):
        if grid[r][col] == 0:
            return r
    return -1

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    moved = np.zeros_like(input_grid, dtype=bool) # track if pixel has moved
    
    # copy the grey cells first
    for r in range(rows):
      for c in range(cols):
        if input_grid[r][c] == 5:
            output_grid[r][c] = 5
            moved[r,c] = True

    # Iterate through non-grey, non-white cells
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] not in (0, 5) and not moved[r,c]:
                val = input_grid[r][c]
                
                # Check for grey above
                grey_above = find_nearest_grey_above(input_grid, r, c)
                if grey_above != -1:
                    empty_above = find_first_empty_above(input_grid, grey_above, c)
                    if empty_above != -1:
                        output_grid[empty_above][c] = val
                        moved[r,c] = True
                        if c+1 < cols and input_grid[r,c+1] != 0:
                           grey_neighbor_above = find_nearest_grey_above(input_grid,r,c+1)
                           if grey_neighbor_above != -1:
                              empty_neighbor = find_first_empty_above(input_grid, grey_neighbor_above, c+1)
                              output_grid[empty_neighbor][c+1] = input_grid[r][c+1]
                              moved[r,c+1] = True
                        continue
                           

                # Check for grey below
                grey_below = find_nearest_grey_below(input_grid, r, c)
                if grey_below != -1:
                    empty_below = find_first_empty_below(input_grid, grey_below +1 , c)
                    if empty_below != -1:
                        output_grid[empty_below][c] = val
                        moved[r,c] = True
                        continue

    # copy unmoved
    for r in range(rows):
        for c in range(cols):
           if not moved[r,c]:
              output_grid[r][c] = input_grid[r][c]

    return output_grid