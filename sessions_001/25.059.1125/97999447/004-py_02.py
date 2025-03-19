"""
Identify non-zero pixels in the input grid. For each, copy to output, then
fill the rest of its row with alternating original and gray color pixels.
"""

import numpy as np

def get_colored_pixels(grid):
    # find the coordinates of the non-white color pixels
    coords = np.argwhere(grid != 0)
    return [((x,y), grid[x,y]) for x, y in coords]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    colored_pixels = get_colored_pixels(input_grid)

    # change output pixels 
    for coord, value in colored_pixels:
        x, y = coord
        output_grid[x,y] = value # copy the pixel to output
        
        # begin fill to right of copied pixel
        fill_color = 5 # gray
        current_col = y + 1
        while current_col < output_grid.shape[1]:
           output_grid[x, current_col] = fill_color
           current_col += 1
           # swap colors
           fill_color = value if fill_color == 5 else 5


    return output_grid