"""
1.  **Double Dimensions:** The input grid's dimensions (height and width) are doubled to create the output grid's dimensions.
2. **Replicate original pixels:** Each pixel in the input grid is replicated in output grid in a 2x2 pattern of cells.
3. **Translate the replicates:** The replicates are at a position 2x their index in both the x and y.
4.  **Fill:** Fill the remaining cells with azure (8).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.full((output_height, output_width), 8, dtype=int)

    # change output pixels 
    for row in range(input_height):
      for col in range(input_width):
        #replicate and translate input pixels
        output_grid[row*2, col*2] = input_grid[row,col]
        

    return output_grid