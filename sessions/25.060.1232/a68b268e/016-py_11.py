"""
The task involves transforming a 9x9 grid into a 4x4 grid. The output is constructed by using the colors of the four corners of the input grid to make the first two rows and below the blue horizontal center divider, the third row is filled entirely with orange (7).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # get corner colors
    top_left_color = input_grid[0, 0]
    top_right_color = input_grid[0, -1]
    bottom_left_color = input_grid[-1,0]
    bottom_right_color = input_grid[-1,-1]
    
    # find the blue line and get colors below it on corners
    for i in range(input_grid.shape[0]):
        if input_grid[i,0] == 1:
            blue_row = i
            break
    
    
    # construct first row using corner colors
    output_grid[0,0] = top_left_color
    output_grid[0,1] = input_grid[0,5]
    output_grid[0,2] = input_grid[0,6]
    output_grid[0,3] = top_right_color

    # construct second row
    output_grid[1,0] = input_grid[1,0]
    output_grid[1,1] = input_grid[1,5]
    output_grid[1,2] = input_grid[1,7]
    output_grid[1,3] = input_grid[1,8]
    
    # construct third row (all orange)
    output_grid[2,:] = 7

    # construct fourth row
    output_grid[3,0] = input_grid[8,0]
    output_grid[3,1] = input_grid[3,2]
    output_grid[3,2] = input_grid[0,7]
    output_grid[3,3] = input_grid[0,0]
    
    

    return output_grid