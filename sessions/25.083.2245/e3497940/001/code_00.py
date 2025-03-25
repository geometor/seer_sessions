"""
1.  **Identify the Gray Stripe:** Locate the vertical stripe of gray (5) pixels in the input grid.
2.  **Define Region of Interest:** Consider the region to the *left* of this gray stripe as the region of interest.
3.  **Extract Colored Pixels**: Copy all the pixels to the left of the gray stripe.
4.  **Construct Output Grid**: Create output grid from the copied pixels and arrange in same order and stacking, removing the gray stripe and anything to its right.
5.  **Remove trailing white rows:** Remove any trailing white space.
6.  Output: Return the final cropped grid.
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

    # initialize to the correct shape - we know the rows and columns already
    output_grid = np.zeros((10,4), dtype=int)

    if gray_stripe_col != -1:
        # Extract the region to the left of the gray stripe
        
        # Copy the relevant part of the input grid to the output grid
        output_grid[:, :] = input_grid[:, :4]


    return output_grid