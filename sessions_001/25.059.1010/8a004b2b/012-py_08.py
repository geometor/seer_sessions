"""
1.  **Iterate Rows:** Process each row of the input grid from top to bottom.

2.  **Horizontal Blue Connection:** Within each row, locate all blue (1) pixels. If two blue pixels are on the same row and all pixels between them are white (0), connect them by changing the intermediate white pixels to blue (1).

3.  **Iterate Columns:** After processing all rows, iterate through the grid by columns, from left to right.

4.  **Vertical Blue Merge:** Within each column, locate all blue pixels. Merge adjacent blocks.

5. **Preserve All Pixels** during the row and column operations, preserve all pixels by copying the input to the output.

6.  **Output:** The output grid should be the same dimensions as the input grid, with the transformations applied.
"""

import numpy as np

def connect_blue_horizontally(grid):
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    blue_pixels = np.argwhere(grid == 1)

    for r in range(rows):
        blue_in_row = [bp for bp in blue_pixels if bp[0] == r]
        if len(blue_in_row) > 1:
            blue_in_row.sort(key=lambda x: x[1])
            for i in range(len(blue_in_row) - 1):
                x1, y1 = blue_in_row[i]
                x2, y2 = blue_in_row[i + 1]
                can_connect = True
                for c in range(y1 + 1, y2):
                    if grid[r, c] != 0:
                        can_connect = False
                        break
                if can_connect:
                    for c in range(y1 + 1, y2):
                        output_grid[r, c] = 1
    return output_grid

def merge_blue_vertically(grid):
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    blue_pixels = np.argwhere(grid == 1)
    
    visited = np.zeros_like(grid,dtype=bool)

    for c in range(cols):
      blue_in_col = [bp for bp in blue_pixels if bp[1] == c]
      if len(blue_in_col) > 1:
        blue_in_col.sort(key=lambda x: x[0])

        for i in range(len(blue_in_col)-1):
            r1,c1 = blue_in_col[i]
            r2,c2 = blue_in_col[i+1]
            can_connect = True
            for r in range(r1+1,r2):
              if grid[r,c] != 0:
                can_connect = False
                break
            if can_connect:
                for r in range(r1 + 1, r2):
                    output_grid[r, c] = 1
    return output_grid

def transform(input_grid):
    # initialize output_grid with the input grid
    grid = np.array(input_grid)
    output_grid = np.copy(grid)

    # Horizontal blue connection
    output_grid = connect_blue_horizontally(output_grid)

    # Vertical blue merging
    output_grid = merge_blue_vertically(output_grid)

    return output_grid.tolist()