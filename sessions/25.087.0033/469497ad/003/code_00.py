"""
Transforms an input grid based on the following rules:
1. Determine the scaling factor 'N' by counting the number of unique non-white (non-zero) colors in the input grid.
2. Create an output grid with dimensions N times the dimensions of the input grid.
3. For each pixel in the input grid at (r, c) with color C:
    a. If C is white (0), the corresponding N x N block in the output grid (starting at N*r, N*c) is filled with white (0), and the pixels on the anti-diagonal of this block are set to red (2).
    b. If C is non-white (C > 0), the corresponding N x N block in the output grid is filled entirely with color C.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Upscales an input grid by a factor N, where N is the number of unique non-white colors.
    Non-white pixels are expanded into solid NxN blocks.
    White pixels are expanded into NxN white blocks with a red anti-diagonal.
    """

    # Convert input_grid to numpy array if it's not already
    input_grid = np.array(input_grid)

    # 1. Calculate the scaling factor N
    unique_colors = np.unique(input_grid)
    non_white_colors = unique_colors[unique_colors != 0]
    n = len(non_white_colors)

    # Handle edge case where n might be 0 if the input grid is all white.
    # Based on examples, n is always >= 1. If it were 0, N=1 seems a reasonable default.
    if n == 0:
        n = 1

    # 2. Get input dimensions and calculate output dimensions
    input_height, input_width = input_grid.shape
    output_height = n * input_height
    output_width = n * input_width

    # 3. Initialize the output grid with white (0)
    #    This handles the background for Rule 3a automatically.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 4. Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            input_color = input_grid[r, c]

            # Define the top-left corner of the N x N block in the output grid
            start_row = n * r
            start_col = n * c

            # 5. Apply transformation rules based on input pixel color
            if input_color == 0:
                # Rule 3a: Block is already white. Set anti-diagonal to red (2).
                # The anti-diagonal elements (i, j) within the block satisfy j = n - 1 - i.
                for i in range(n):
                    # Calculate the absolute coordinates in the output grid
                    out_r = start_row + i
                    out_c = start_col + (n - 1 - i)
                    # Ensure we don't go out of bounds (should not happen with correct dimensions)
                    if 0 <= out_r < output_height and 0 <= out_c < output_width:
                         output_grid[out_r, out_c] = 2 # red
            else:
                # Rule 3b: Fill the N x N block with the non-white input color.
                output_grid[start_row : start_row + n, start_col : start_col + n] = input_color

    return output_grid