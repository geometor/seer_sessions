import numpy as np

"""
Transformation rule:
1. Receive the input grid, which is a single row of pixels. Let its width be W.
2. Count the number of pixels C in the input row that are not white (color code 0).
3. Calculate the dimension N for the square output grid by multiplying C by W (N = C * W).
4. Create a new square grid of size N x N, initialized with white (0).
5. Iterate through each pixel of the input row using its index k (from 0 to W-1). Let the color be color_k.
6. For the current index k and color_k, iterate through each row r of the output grid (from r = 0 to N-1).
7. Calculate the target column c using the formula: c = (N - 1) + k - r.
8. If c is within the bounds (0 <= c < N), update the output grid pixel at (r, c) to color_k.
9. Return the final N x N grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms a 1xW input grid into an NxN output grid by stamping the input
    row diagonally. N is calculated based on the number of non-white pixels
    in the input.
    """
    # Ensure input is a 2D numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Check if input is indeed a single row
    if input_grid.shape[0] != 1:
        raise ValueError("Input grid must have exactly one row.")

    input_row = input_grid[0]
    W = len(input_row) # Width of the input row

    # Count non-white pixels (C)
    non_white_pixels = input_row[input_row != 0]
    C = len(non_white_pixels)

    # Handle edge case where C=0 (no non-white pixels)
    # Although not explicitly shown in examples, a 0x0 grid is problematic.
    # Let's return a 1x1 white grid as a plausible default, or maybe WxW?
    # The pattern N=C*W suggests N=0. Let's stick to the pattern strictly for now.
    # If C=0, N=0. Creating a 0x0 array might cause issues downstream.
    # Based on examples, C is always >= 1. If C=0, let's return a 1x1 white grid.
    if C == 0:
        # Returning a minimal valid grid if no non-white pixels are found.
        # This case is not covered by the examples.
        # An alternative might be to return an empty array or raise an error.
        # Let's choose a 1x1 white grid for now.
        return np.zeros((1, 1), dtype=int)


    # Calculate output dimension N
    N = C * W

    # Create an NxN output grid initialized with white (0)
    output_grid = np.zeros((N, N), dtype=int)

    # Iterate through each pixel of the input row
    for k in range(W):
        color_k = input_row[k]
        # No need to process white pixels from input, as output is already white
        # and overwriting prioritizes later (higher k) pixels anyway.
        # But the logic works even including white pixels, just slightly less efficient.
        # Let's include them for direct implementation of the derived rule.

        # Iterate through each row r of the output grid
        for r in range(N):
            # Calculate the target column c
            c = (N - 1) + k - r

            # Check if c is within the bounds of the output grid
            if 0 <= c < N:
                # Update the pixel at (r, c) with the color from the input
                # Note: Pixels with higher k (further right in input) will overwrite
                # pixels with lower k if they map to the same output coordinate.
                output_grid[r, c] = color_k

    return output_grid