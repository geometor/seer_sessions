"""
The transformation rule involves expanding a 3x3 input grid into a 9x9 output grid. 
Non-white pixels in the input grid trigger the creation of 4x4 blocks of the same color in the output grid.
If the input block contains a mix of colors, the top-left most color is used for expansion. The remaining output grid is filled with white (0).
"""

import numpy as np

def get_top_left_non_white(grid):
    """Find the top-left non-white pixel and its color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return (r,c), grid[r,c]
    return None, 0

def transform(input_grid):
    # initialize output_grid as 9x9 filled with white (0)
    output_grid = np.zeros((9, 9), dtype=int)

    # Find the top-left most non-white pixel and its color
    top_left_coords, top_left_color = get_top_left_non_white(input_grid)
    if top_left_coords is not None:
       r,c = top_left_coords
       offset_r = r*3
       offset_c = c*3
       output_grid[offset_r:offset_r+4, offset_c:offset_c+4] = top_left_color

    
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
             if input_grid[r,c] != 0:
                offset_r = r*3
                offset_c = c*3
                #print(offset_r, offset_c)
                output_grid[offset_r:offset_r+4, offset_c:offset_c+4] = input_grid[r,c] # set the color to the input pixels colors
    
    # Find the top-left most non-white pixel, after initial scan and its color
    top_left_coords, top_left_color = get_top_left_non_white(input_grid)

    # iterate the entire input grid
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:  # if we found a non-white pixel
               
                #first lets grab the color of that pixel
                pixel_color = input_grid[r,c]

                # Check adjacent, non-white pixel
                # look up one row
                if(r-1 >= 0 and input_grid[r-1,c] !=0):
                    pixel_color = input_grid[r-1,c]
                # look left one column
                if(c-1 >= 0 and input_grid[r,c-1] != 0):
                    pixel_color = input_grid[r,c-1]
                
                #set offset
                offset_r = r*3
                offset_c = c*3

                output_grid[offset_r:offset_r+4, offset_c:offset_c+4] = pixel_color # corrected color
    return output_grid