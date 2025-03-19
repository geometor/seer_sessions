"""
1.  **Identify existing colored regions**: Locate the existing green (3), white (0) and maroon (9) regions within the 6x6 input grid.
2.  **Locate target area**: Identify the bottom-right corner of the grid.
3.  **Place new object**: add a small green "L" consisting of two pixels.
4.   add the "L" shape to the bottom right, ensuring all added green values maintain the shape of an L.
5.  Copy all other values, creating a new array and returning it.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # get dimensions
    height = output_grid.shape[0]
    width = output_grid.shape[1]


    # add two green pixels in L shape at bottom right.
    output_grid[height-2, width-2] = 3
    output_grid[height-1, width-1] = 3
    

    return output_grid