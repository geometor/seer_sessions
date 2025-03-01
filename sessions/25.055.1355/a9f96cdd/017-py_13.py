"""
1.  Identify Red Pixels: Locate all pixels with a value of 2 (red) in the input grid.
2.  Place Azure and Orange:** For *each* red pixel:
    *   If the red pixel is *not* in the first column (x=0), place an azure (8) pixel directly to its left (x-1) in the same row.
    *    If the red is in the first column, place the azure in this column and the red one space to the right.
    *   If the red pixel is *not* in the last column, place an orange (7) pixel directly to its right (x+1) in the same row.
    *   If the red is in the last column, the orange is placed at that position, the red does not change.
3.  Preserve Red:** The red pixel itself remains in the *same* position in the output grid as in the input grid, unless at an edge.
4. **Copy other pixels:** All non red colors from input are discarded.
"""

import numpy as np

def get_pixel_positions(grid, color):
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Identify Red Pixels
    red_pixels = get_pixel_positions(input_grid, 2)

    # Place Azure and Orange and Red
    for row, col in red_pixels:
        # Handle Azure placement (left)
        if col > 0:
          output_grid[row, col - 1] = 8  # Place azure to the left
          output_grid[row, col] = 2      # place red
        else:
          output_grid[row, col] = 8 # Place azure in first column
          if col + 1 < cols:
            output_grid[row, col + 1] = 2  # shift red right
          
        # Handle Orange placement (right)
        if col < cols - 1:
            if col > 0:
              output_grid[row, col + 1] = 7  # Place orange to the right
            else:
               if col + 2 < cols:
                 output_grid[row,col + 2] = 7
        else:
            output_grid[row, col] = 7 #place orange, red is unchanged

    return output_grid