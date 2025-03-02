"""
1.  **Identify Blue Stripe:** Scan the input grid to find a vertical stripe of blue (1) pixels. A column qualifies as a blue stripe if it contains *at least one* blue pixel. If no such stripe is found, the output is a grid of the same dimensions as the input, filled entirely with white (0).

2.  **Determine Output Dimensions and ROI:** If a blue stripe is found:
    *   The output grid's height is always 5.
    *   The output grid's width is determined as follows:
        *   If any blue pixel exists in column 1 or column 2, then output width is
            4
        *   If no blue pixels exist in columns 1 or 2, and a blue stripe exists,
            then scan from right to left to find the *first* (rightmost) blue
            pixel, and if found in the last two columns of the input grid, then the width is 4.
        *    Otherwise the width is 5.
    *   The Region of Interest (ROI) starts at a calculated column:
        *  If the width is 5, the ROI starts 2 columns to the left of the
           *leftmost* blue stripe, but clamped to a minimum start of column 0
           and maximum start large enough to include the entire width.
        *  If the width is 4, and the *leftmost* blue pixel is in column 1 or 2, the ROI starts at column 0.
        *  If the width is 4, and the *rightmost* blue pixel is in the last two columns, then start at that position - 3
           

3.  **Color Mapping:** Within the ROI:
    *   Any pixel that is blue (1) in the input grid becomes azure (8) in the output grid.
    *   All other pixels within the ROI become white (0).

4.  **Output:** The resulting `output_grid` is the transformed grid.
"""

import numpy as np

def find_leftmost_blue_stripe(grid):
    # Find the column index of the leftmost blue stripe (color 1).
    for j in range(grid.shape[1]):
        if np.any(grid[:, j] == 1):
            return j
    return -1

def find_rightmost_blue_stripe(grid):
  # Find the column index of the rightmost blue stripe.
    for j in range(grid.shape[1] -1, -1, -1):
      if np.any(grid[:,j] == 1):
        return j
    return -1

def transform(input_grid):
    # Find the column index of the leftmost blue stripe (color 1).
    leftmost_stripe_col = find_leftmost_blue_stripe(input_grid)

    # Handle absence of stripe.
    if leftmost_stripe_col == -1:
        output_grid = np.zeros_like(input_grid)
        return output_grid

    # Determine output dimensions.
    output_height = 5
    rightmost_stripe_col = find_rightmost_blue_stripe(input_grid)
    input_width = input_grid.shape[1]

    if np.any(input_grid[:, :2] == 1):
      output_width = 4
    elif rightmost_stripe_col >= input_width - 2:
      output_width = 4
    else:
       output_width = 5

    # Determine ROI start column.
    if output_width == 5:
        start_col = max(0, leftmost_stripe_col - 2)
        start_col = min(start_col, input_width - output_width)  #clamp
    elif output_width == 4 and leftmost_stripe_col in [0,1]:
       start_col = 0
    elif output_width == 4:
       start_col = rightmost_stripe_col - 3

    # Initialize the output grid with all zeros (white).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate and map colors.
    for i in range(min(output_height, input_grid.shape[0])):
        for j in range(output_width):
            input_j = start_col + j
            if 0 <= input_j < input_grid.shape[1]:
                if input_grid[i, input_j] == 1:
                    output_grid[i, j] = 8

    return output_grid