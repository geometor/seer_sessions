import numpy as np

"""
Transforms an input grid based on the following rules:
1. Determine the scaling factor 'N' by counting the number of unique non-white (non-zero) colors in the input grid. If no non-white colors exist, N defaults to 1.
2. Create an output grid with dimensions N times the dimensions of the input grid.
3. Iterate through each pixel in the input grid at (r, c) with color C:
    a. If C is non-white (C > 0), the corresponding N x N block in the output grid (starting at N*r, N*c) is filled entirely with color C.
    b. If C is white (C == 0):
        i. The corresponding N x N block in the output grid is initialized to white (0).
        ii. If N is odd, the pixels on the *main* anti-diagonal of this block (indices i, N-1-i relative to the block's top-left corner) are set to red (2).
        iii. If N is even, the pixels on the *main* diagonal of this block (indices i, i relative to the block's top-left corner) are set to red (2).
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Upscales an input grid by a factor N, where N is the number of unique non-white colors.
    Non-white pixels are expanded into solid NxN blocks.
    White pixels are expanded into NxN white blocks with either a red main diagonal (if N is even)
    or a red anti-diagonal (if N is odd).
    """

    # Convert input_grid to numpy array if it's not already
    input_grid = np.array(input_grid)

    # 1. Calculate the scaling factor N
    unique_colors = np.unique(input_grid)
    non_white_colors = unique_colors[unique_colors != 0]
    n = len(non_white_colors)

    # Handle edge case where n might be 0 if the input grid is all white.
    # Based on examples, n is always >= 1. If it were 0, N=1 seems a reasonable default,
    # which would result in an anti-diagonal (since N=1 is odd).
    if n == 0:
        n = 1 # Default scaling factor if no non-white colors

    # 2. Get input dimensions and calculate output dimensions
    input_height, input_width = input_grid.shape
    output_height = n * input_height
    output_width = n * input_width

    # 3. Initialize the output grid with white (0)
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
                # Rule 3b: Block is already initialized to white. Determine which diagonal to make red.
                # Iterate *within* the N x N block to draw the diagonal.
                if n % 2 == 0:
                    # N is even: Set main diagonal to red (2).
                    # The main diagonal elements (i, j) within the block satisfy j = i.
                    for i in range(n):
                        out_r = start_row + i
                        out_c = start_col + i
                        # Boundary check (though should be unnecessary with correct dimensions)
                        if 0 <= out_r < output_height and 0 <= out_c < output_width:
                             output_grid[out_r, out_c] = 2 # red
                else:
                    # N is odd: Set anti-diagonal to red (2).
                    # The anti-diagonal elements (i, j) within the block satisfy j = n - 1 - i.
                    for i in range(n):
                        out_r = start_row + i
                        out_c = start_col + (n - 1 - i)
                        # Boundary check
                        if 0 <= out_r < output_height and 0 <= out_c < output_width:
                             output_grid[out_r, out_c] = 2 # red
            else:
                # Rule 3a: Fill the N x N block with the non-white input color.
                output_grid[start_row : start_row + n, start_col : start_col + n] = input_color

    return output_grid