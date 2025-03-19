"""
The input grid is expanded into a larger grid by replicating each pixel
to create 2x2 blocks. Then the output structure is formed by the original
cross and a mirrored structure

1.  **Initialization:** Create an empty 6x6 output grid.

2.  **Cross Replication:** For each cell (x, y) in the 3x3 input grid,
    copy its value to the output grid at positions: (x,y) and also add the
    original row and column to the output grid forming a cross.

3.  **Mirror:** Complete the output by mirroring each input pixel.
    specifically the output is the result of copying the input,
    interleaved with a 90-degree rotated copy of the input.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as 6x6 with zeros
    output_grid = np.zeros((6, 6), dtype=int)

    # Iterate through the input grid
    for row in range(3):
        for col in range(3):
            # Copy each pixel value
            pixel_value = input_grid[row, col]

            # set 2x2 block in output
            output_grid[row * 2, col * 2] = pixel_value

            # mirror and rotate the input grid using the transposed pixel value
            output_grid[col * 2 + 1, row * 2 ] = pixel_value
            output_grid[col * 2 , row * 2 + 1] = pixel_value
            output_grid[row * 2 + 1, col * 2+1] = pixel_value


    return output_grid