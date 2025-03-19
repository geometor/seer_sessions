"""
1.  **Identify Borders:** Locate the top and bottom rows of the input grid. Note their colors, as these "border" rows remain unchanged in the output.
2.  **Isolate Interior:** Consider the region of the grid excluding the top and bottom border rows.
3.  **Background**: Inside the grid (excluding borders), the output grid contains large areas of white (0).
4. **Identify Significant Pixels**: find any non-white pixel in the interior.
5.  **Transformation Rule:**
   For each non-white pixel inside the grid,
    * If the identified color is in the same column as a border color, duplicate it.
    * If the pixel's color in the same row as the border color, move it to the right
    * All other identified pixels should be removed, being converted to the background.
"""

import numpy as np

def get_borders(grid):
    top_border = grid[0, :].copy()
    bottom_border = grid[-1, :].copy()
    return top_border, bottom_border

def find_significant_pixels(grid, top_border, bottom_border):
    significant_pixels = []
    for r in range(1, grid.shape[0] - 1):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                significant_pixels.append((r, c, grid[r, c]))
    return significant_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # get border colors
    top_border, bottom_border = get_borders(input_grid)

    # copy borders to the output grid
    output_grid[0, :] = top_border
    output_grid[-1, :] = bottom_border
    
    # Identify significant pixels in the interior
    significant_pixels = find_significant_pixels(input_grid, top_border, bottom_border)

    # Apply transformation rule
    for r, c, color in significant_pixels:
        top_border_color = input_grid[0,c]
        bottom_border_color = input_grid[-1,c]
        
        left_border_color = input_grid[r,0]
        right_border_color = input_grid[r,-1]

        if color == top_border_color or color == bottom_border_color:
            output_grid[r,c] = color #duplicate
            #duplicate on the same column
            if(r + 1 <  output_grid.shape[0] -1):
                output_grid[r + 1,c] = color
        elif color == left_border_color or color == right_border_color:
             #move right on the same row.
            if(c + 1 < output_grid.shape[1] -1 ):
                 output_grid[r,c + 1] = color
        #else background, already 0

    return output_grid