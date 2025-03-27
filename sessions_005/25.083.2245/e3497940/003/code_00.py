"""
1.  **Locate the Gray Stripe:** Find the vertical stripe of gray (5) pixels in the input grid. This stripe acts as a dividing line.
2.  **Determine the Region of Interest** Determine the column location to the left of the gray stripe.
3.  **Extract Pixels:** Copy all of the pixels to the left of the gray stripe in the input grid.
4.  **Construct Output Grid:** Create an output grid with number of rows equal to the input grid and number of columns equal to the location of the left edge of the gray stripe. Copy the colors from the left side of the gray stripe on the input grid to this new output grid, maintaining the order and relative positions of the pixels.
5.  **Output:** Return the final output grid.
"""

import numpy as np

def find_gray_stripe_column(grid):
    """Finds the column index of the gray stripe."""
    rows, cols = grid.shape
    for j in range(cols):
        # Check if the entire column is gray (5)
        if np.all(grid[:, j] == 5):
            return j
    return -1  # Stripe not found

def transform(input_grid):
    """Transforms the input grid by extracting the region to the left of the gray stripe."""
    # Find the column index of the gray stripe
    gray_stripe_col = find_gray_stripe_column(input_grid)

    if gray_stripe_col == -1:  # handle no stripe found
        return input_grid

    # Determine the dimensions of the output grid
    num_rows = input_grid.shape[0]
    num_cols = gray_stripe_col

    # Initialize the output grid
    output_grid = np.zeros((num_rows, num_cols), dtype=int)

    # Copy the relevant part of the input grid to the output grid
    if num_cols > 0: # must have columns to copy
       output_grid[:, :] = input_grid[:, :num_cols]

    return output_grid