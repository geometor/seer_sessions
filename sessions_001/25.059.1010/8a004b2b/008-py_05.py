"""
1.  **Crop:** Remove the outer rows and columns of the input grid that consist entirely of white (0) pixels, stopping when a non-white pixel in any row or column is met.
2.  **Condense Blue:** Within the cropped region, locate all blue (1) squares. If multiple blue squares are adjacent horizontally or vertically, condense or connect those. Horizontal blue blocks attempt to connect by filling a line between the blocks if all colors inbetween are white. Vertical condensation simply merges contiguous vertically aligned blocks. Diagonal and isolated squares do not get condensed.
3. **Preserve other colors:** Other colored squares (red, green, yellow) are preserved from the cropped input to the output without modification to position or dimension, in the same absolute positions relative to each other.
"""

import numpy as np

def crop_grid(grid):
    rows, cols = grid.shape
    top, bottom, left, right = 0, rows, 0, cols

    # Find top boundary
    for i in range(rows):
        if np.any(grid[i, :] != 0):
            top = i
            break

    # Find bottom boundary
    for i in range(rows - 1, -1, -1):
        if np.any(grid[i, :] != 0):
            bottom = i + 1
            break

    # Find left boundary
    for j in range(cols):
        if np.any(grid[:, j] != 0):
            left = j
            break

    # Find right boundary
    for j in range(cols - 1, -1, -1):
        if np.any(grid[:, j] != 0):
            right = j + 1
            break

    return grid[top:bottom, left:right], top, left

def condense_blue(grid, top_offset, left_offset):
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    blue_pixels = np.argwhere(grid == 1)

    # horizontal condensation
    for r in range(rows):
      blue_in_row = [bp for bp in blue_pixels if bp[0] == r]
      if len(blue_in_row)>1:
        blue_in_row.sort(key=lambda x: x[1])
        for i in range(len(blue_in_row) - 1):
          x1, y1 = blue_in_row[i]
          x2, y2 = blue_in_row[i+1]
          can_connect = True
          for c in range(y1 + 1, y2):
            if grid[r,c] != 0:
              can_connect = False
              break
          if can_connect:
            for c in range(y1,y2+1):
              output_grid[r,c] = 1

    # vertical condensation - check contiguous only
    visited = np.zeros_like(grid, dtype=bool)
    for r, c in blue_pixels:
      if visited[r,c] == False:
        visited[r,c] = True
        count_v = 0
        for i in range(r + 1, rows):
            if grid[i, c] == 1:
                count_v +=1
                visited[i,c] = True
            else:
                break
        if count_v>0: # there are vertical neighbors to merge
          for v in range(count_v+1):
            output_grid[r+v,c]=1

    return output_grid
def transform(input_grid):
    # Crop the input grid
    cropped_grid, top_offset, left_offset = crop_grid(np.array(input_grid))

    # Condense blue pixels and keep track of changes
    condensed_grid = condense_blue(cropped_grid, top_offset, left_offset)

    # initialize output
    rows, cols = condensed_grid.shape
    output_grid = np.zeros((rows,cols), dtype=int)
    for r in range(rows):
      for c in range(cols):
        output_grid[r,c] = condensed_grid[r,c]

    return output_grid.tolist()