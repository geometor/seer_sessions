import numpy as np

# Constants for colors
WHITE = 0
GREY = 5
AZURE = 8

def find_first_white_pixel(grid_np):
    """
    Finds the coordinates (row, column) of the top-most, then left-most
    white pixel (0) within the inner grid (excluding the border).
    Returns (None, None) if no white pixel is found.
    """
    h, w = grid_np.shape
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            if grid_np[r, c] == WHITE:
                return r, c
    return None, None # Should not happen based on examples

def transform(input_grid):
    """
    Transforms the input grid by changing specific white pixels (0) to azure (8)
    along a determined diagonal path within the grey (5) border.

    The diagonal path is determined based on the colors of the inner corner pixels
    or the location of the first white pixel found (top-to-bottom, left-to-right).

    1. If inner top-left (1,1) is white, use the main diagonal (r == c).
    2. Else if inner top-right (1, W-2) is white, use the anti-diagonal (r + c == W - 1).
    3. Else, find the first white pixel (r_min, c_min) and use the diagonal c = r + (c_min - r_min).
    """

    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_np = np.copy(input_np)
    h, w = input_np.shape

    # Check conditions to determine the diagonal path
    # Condition 1: Inner top-left corner is white
    if input_np[1, 1] == WHITE:
        # Iterate through the inner grid along the main diagonal
        for i in range(1, min(h - 1, w - 1)):
            if input_np[i, i] == WHITE:
                output_np[i, i] = AZURE

    # Condition 2: Inner top-left is not white, but inner top-right is white
    elif input_np[1, w - 2] == WHITE:
        # Iterate through the inner grid along the anti-diagonal
        diag_sum = w - 1 # r + c = constant for anti-diagonal passing through (1, w-2) and (h-2, 1)
                        # For a path through (1, w-2), the sum is 1 + (w-2) = w-1
        for r in range(1, h - 1):
            c = diag_sum - r
            # Check if the column index is within the inner grid bounds
            if 1 <= c < w - 1:
                if input_np[r, c] == WHITE:
                    output_np[r, c] = AZURE

    # Condition 3: Neither inner top corner is white
    else:
        # Find the first white pixel (top-most, then left-most) in the inner grid
        r_min, c_min = find_first_white_pixel(input_np)

        # If a white pixel was found (it should be, based on examples)
        if r_min is not None:
            # Calculate the diagonal constant k = c - r
            k = c_min - r_min
            # Iterate through the inner grid along the diagonal c = r + k
            for r in range(1, h - 1):
                c = r + k
                # Check if the column index is within the inner grid bounds
                if 1 <= c < w - 1:
                    if input_np[r, c] == WHITE:
                        output_np[r, c] = AZURE

    # Convert the NumPy array back to a list of lists for the final output
    return output_np.tolist()