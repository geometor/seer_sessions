"""
1.  **Initialization:**
    *   Determine the height of the output grid. It appears to be related to the position of red in the input. Specifically, `output_height = input_width * 2 - (input_width - x_last_red) -  3 ` where `x_last_red` is the column of the last red pixel in the first row of input.
    *   Create an output grid filled with white pixels (0). The output grid's width is always 7.

2.  **Green Pixel:**
    *   Place a single green pixel (3) at position (0, 3) in the output grid (row 1, column 4).

3.  **Red Stripes:**
    * Find the x-coordinates (column indices) of *all* red pixels (2) in the *input* grid.
    *   For each of those `x` values:
        * Place a vertical stripe of red pixels (2) in the *output* grid.
        * The stripes in all examples starts at y=3.
        *   The end row of the stripe changes based on each example.
            - The length of the first red stripe from left equals to the height of output
            - If there is another red stripe:
              The length of second stripe is `output_height - input_width + x_position` where x is the first red pixel from the left.
    * We can describe the length of n-th stripe (if available) in a generic way: `output_height - (n-1) * (input_width - x_position_of_red_pixel_on_top_row)`
"""

import numpy as np

def get_red_x_positions(grid):
    """Finds the x-coordinates of all red pixels in the grid."""
    return [i for i in range(grid.shape[1]) if 2 in grid[:,i]]

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    
    red_x_positions = get_red_x_positions(input_grid)
    if (len(red_x_positions) > 0):
      x_last_red = max(red_x_positions)
      output_height = input_width * 2 - (input_width - x_last_red) +1 - 3
    else:
       output_height = 0 # special case if no red

    output_width = 7
    output_grid = np.zeros((max(output_height,0), output_width), dtype=int)

    if output_height == 0:
       return output_grid

    # Place green pixel
    output_grid[0, 3] = 3


    # Place red stripes

    for n, x in enumerate(red_x_positions):
        start_row = 3
        
        if n == 0: #first
          end_row = output_height
        
        elif len(red_x_positions) > 1:
          first_red_x = min(red_x_positions)
          end_row = output_height - (input_width - first_red_x -1)
        else:
           end_row = output_height
       
        for y in range(start_row, end_row):
            output_grid[y, x] = 2
    

    return output_grid