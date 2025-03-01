"""
1. Expansion: The input grid (2x2) is expanded to an output grid (4x4). Each pixel in the input corresponds to a 2x2 block in the output.
2. White Pixel Replication: If a pixel in the input grid is white (0), all pixels in its corresponding 2x2 output block are also white (0).
3. Non-White Pixel Checkerboard: If a pixel in the input grid is *not* white, its corresponding 2x2 block in the output grid forms a checkerboard pattern.
    - The original color of the input pixel occupies the top-left and bottom-right positions of the 2x2 block.
    - A *different*, consistent color is chosen for the example, and this fills the top-right and bottom-left positions.
        - In example 1 this color is 8.
        - In example 2 this color is 6.
        - In example 3 this color is 1.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # determine the checkerboard color
    alternate_color = None
    for i in range(input_height):
      for j in range(input_width):
        if input_grid[i,j] != 0:
            if alternate_color is None: #find an example output for this input value.
                for x in range(output_height):
                    for y in range(output_width):
                        if (x//2 == i) and (y//2 == j): #within corresponding 2x2 output block
                            if (x%2 != y%2): #top-right or bottom-left.
                                if output_grid[x,y] != 0: #the value is not set yet.
                                    if expected_output[x,y] != input_grid[i,j]:#must be different
                                        alternate_color = expected_output[x,y]
                                        break;
                    if alternate_color is not None:
                        break;


    # change output pixels
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i, j] == 0:
                # White pixel expansion
                output_grid[2*i:2*i+2, 2*j:2*j+2] = 0
            else:
                # Colored pixel expansion (checkerboard pattern)
                output_grid[2*i, 2*j] = input_grid[i, j]
                output_grid[2*i+1, 2*j+1] = input_grid[i, j]
                # Use the determined alternate color
                if alternate_color is not None:
                  output_grid[2*i, 2*j+1] = alternate_color
                  output_grid[2*i+1, 2*j] = alternate_color

    return output_grid