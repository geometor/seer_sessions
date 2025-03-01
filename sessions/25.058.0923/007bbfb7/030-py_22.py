"""
1.  **Determine Output Grid Size:** The output grid's height is calculated as `(input_grid height * 2) + 1` if the height is less than 4 and `(input_grid height * 2) -1`
    otherwise. The width is `input_grid width * (input_grid height)` if height is
    less than 4, otherwise `input_grid.width * 2`
2.  **Tile Input Grid:** Copy the entire input grid repeatedly to create the output grid. The tiling is done horizontally and vertically.
    - If the input_grid is less than 4 rows high, stack sections of the input grid as many times as the height. Separate each full grid vertically with a row of zeros.
    - If the input_grid is greater than 3 rows high, the number of horizontal repeats equals 2, the input grid is tiled in full vertically twice, with one row of zeros in-between.
3.  **Insert Empty Rows:** Insert rows filled with white (0) between the tiled input grid sections vertically. There is exactly one empty row between each full replication of the input grid.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Determine Output Grid Size
    if input_height < 4:
        output_height = (input_height * 2) + 1
        output_width = input_width * input_height
    
    else:
        output_height = (input_height * 2) - 1
        output_width = input_width * 2
    
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Tile Input Grid
    if input_height < 4:
        for i in range(input_height):
            for j in range(input_height):
                output_grid[i * 2, j * input_width : (j+1) * input_width] = input_grid[i, :]
    else:
        for i in range(2):
           for j in range(2):
                output_grid[i * (input_height+1)-i*2 : i * (input_height+1)-i*2 +input_height, j*input_width:(j+1)*input_width] = input_grid

    return output_grid