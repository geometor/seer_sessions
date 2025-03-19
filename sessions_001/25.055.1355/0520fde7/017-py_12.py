"""
1.  **Find the Gray Stripe**: Locate the vertical stripe of gray (value 5) pixels in the input grid. Note its column index.
2.  **Initialize Output**: Create a 3x3 output grid filled with black (value 0) pixels.
3.  **Iterate Rows**: For each row in the input grid:
    *   **Check Left**: If there's a blue pixel (value 1) to the *left* of the gray stripe in the current row, place a red pixel (value 2) in the output grid at the same row and column 0.
    *   **Check Right**: If there's a blue pixel (value 1) to the *right* of the gray stripe in the current row, place a red pixel (value 2) in the output grid at the same row and column 1.
4. **Return output**: The output grid will always have dimensions of 3x3.
"""

import numpy as np

def find_gray_stripe_column(grid):
    """Finds the column index of the vertical gray stripe."""
    for col in range(grid.shape[1]):
        if all(grid[:, col] == 5):
            return col
    return -1  # Should not happen based on problem description

def transform(input_grid):
    # Initialize output grid: 3x3 filled with black (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the gray stripe
    gray_stripe_col = find_gray_stripe_column(input_grid)

    # Iterate through each row of the input grid
    for row in range(input_grid.shape[0]):
        # Check for blue pixels to the left of the gray stripe
        if gray_stripe_col > 0:
            for col in range(gray_stripe_col):
                if input_grid[row, col] == 1:
                    output_grid[row, 0] = 2
                    break  # Only one red pixel per row, so break after finding the first blue

        # Check for blue pixels to the right of the gray stripe
        if gray_stripe_col < input_grid.shape[1] - 1:
            for col in range(gray_stripe_col + 1, input_grid.shape[1]):
                if input_grid[row, col] == 1:
                    output_grid[row, 1] = 2
                    break   # Only one red pixel per row, so break after finding the first blue

    return output_grid