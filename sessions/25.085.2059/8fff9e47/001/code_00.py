"""
Scales the input grid to a fixed 12x12 output grid.
Each pixel in the input grid is expanded into a rectangular block
of the same color in the output grid. The dimensions of the block
are determined by the integer scaling factors calculated from the
ratio of output dimensions (12x12) to input dimensions.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by scaling each pixel into a block
    to fit a 12x12 output grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 12x12 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to numpy array if it isn't already
    input_grid_np = np.array(input_grid)

    # 1. Determine the height (H_in) and width (W_in) of the input grid.
    H_in, W_in = input_grid_np.shape

    # 2. Define the target output grid dimensions.
    H_out = 12
    W_out = 12

    # 3. Calculate the integer scaling factor for height.
    # Use integer division //
    Scale_H = H_out // H_in

    # 4. Calculate the integer scaling factor for width.
    Scale_W = W_out // W_in

    # 5. Create a new grid (the output grid) with dimensions H_out x W_out.
    # Initialize with zeros (white).
    output_grid = np.zeros((H_out, W_out), dtype=int)

    # 6. Iterate through each pixel of the input grid.
    for r_in in range(H_in):
        for c_in in range(W_in):
            # Get the color of the current input pixel.
            color = input_grid_np[r_in, c_in]

            # a. Determine the top-left corner coordinates for the corresponding block.
            r_out_start = r_in * Scale_H
            c_out_start = c_in * Scale_W

            # b. Fill the rectangular block in the output grid.
            # Select the slice corresponding to the block.
            # The end indices are exclusive in slicing, so no need for -1.
            output_grid[r_out_start : r_out_start + Scale_H, 
                        c_out_start : c_out_start + Scale_W] = color

    # 7. Return the completed output grid.
    return output_grid