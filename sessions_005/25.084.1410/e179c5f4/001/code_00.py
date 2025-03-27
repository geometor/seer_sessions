import numpy as np

"""
Transforms an input grid into an output grid of the same dimensions. 
The output grid is filled with azure (8) except for a single blue (1) pixel in each row.
The blue pixel follows a vertical zigzag pattern. 
The pattern starts in the first row (row 0) at a column determined by the grid width: 
- If width W is even, start at column W-1.
- If width W is odd, start at column W // 2.
The pattern initially moves left (direction = -1). When it hits either the left (col 0) 
or right (col W-1) edge, the direction reverses.
"""

def transform(input_grid):
    """
    Applies the zigzag transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    H, W = input_grid.shape

    # Initialize output grid filled with azure (8)
    output_grid = np.full((H, W), 8, dtype=int)

    # Calculate the starting column based on width parity
    if W % 2 == 0:
        current_col = W - 1
    else:
        current_col = W // 2

    # Initialize the horizontal movement direction (start moving left)
    direction = -1

    # Iterate through each row to place the blue pixel
    for r in range(H):
        # Set the pixel at the current position to blue (1)
        if 0 <= current_col < W: # Ensure current_col is valid (should always be unless W=0?)
             output_grid[r, current_col] = 1
        else:
             # This case should ideally not happen with the boundary check logic below,
             # but added as a safeguard. If W=1, direction reversal logic handles it.
             pass


        # Calculate the potential next column
        next_col = current_col + direction

        # Check if the next position hits a boundary
        if next_col < 0 or next_col >= W:
            # Reverse direction
            direction *= -1
            # Recalculate the next column with the new direction
            # This ensures the pattern "bounces" off the wall correctly in the same step
            next_col = current_col + direction

        # Update the current column for the next row
        # This handles the case W=1 correctly, where next_col will always be 0 after reversal.
        current_col = next_col


    return output_grid