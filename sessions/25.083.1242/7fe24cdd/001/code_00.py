"""
The output grid is created with dimensions that are twice the width and twice the height of the input grid.
The output grid is conceptually divided into six equal-sized regions, arranged in a 2x3 grid formation (two rows, three columns). Each region is the same size as the input grid.
The input grid is copied to each region.  
Pixel pairs at these coordinates are swapped: (0,0) and (1,1), (0,1) and (1,2), (0,2) and (2,0), (1,0) and (2,1), (1,1) and (2,2).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height
    output_width = 3 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # create a list of pixel data: coordinates and color
    pixel_data = [((row, col), input_grid[row, col])
                  for row in range(input_height)
                  for col in range(input_width)]
    
    # create index pairs for swapping, offset by 4
    pixel_pairs = list(zip(pixel_data, pixel_data[4:]))

    # iterate through the six regions of the output
    for i in range(2):  # row multiplier
        for j in range(3):  # col multiplier
            # copy input grid to each output region
            for row in range(input_height):
                for col in range(input_width):
                    output_grid[i * input_height + row, j * input_width + col] = input_grid[row, col]
            
            # perform pixel swaps based on pixel_pairs
            for (pair1, pair2) in pixel_pairs:
                ((row1, col1), value1) = pair1
                ((row2, col2), value2) = pair2

                # Calculate coordinates in the output grid for current region
                output_row1, output_col1 = i * input_height + row1, j * input_width + col1
                output_row2, output_col2 = i * input_height + row2, j * input_width + col2
                
                # Swap values
                temp = output_grid[output_row1, output_col1]
                output_grid[output_row1, output_col1] = output_grid[output_row2, output_col2]
                output_grid[output_row2, output_col2] = temp

    return output_grid