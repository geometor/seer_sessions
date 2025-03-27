"""
Simulates gravity on a 2D grid of pixels. Non-white pixels fall downwards until they hit the bottom row, the bottom edge of the grid, or another non-white pixel. The bottom-most row of the grid acts as a stable floor and its pixels do not move. The process repeats until no more pixels can fall.
"""

import numpy as np

def transform(input_grid):
    """
    Applies gravity to non-white pixels in the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid after gravity is applied.
    """
    # Convert input grid to a NumPy array for easier manipulation
    output_grid = np.array(input_grid, dtype=int)
    height, width = output_grid.shape

    # The bottom row (index height - 1) is the floor and does not move.
    # We only need to simulate gravity for rows above the floor.

    # Loop until no more pixels can move downwards in a full pass
    while True:
        moved = False  # Flag to track if any pixel moved in this iteration

        # Iterate through the grid from bottom-up (excluding the floor row)
        # Start from the second-to-last row (index height - 2) and go upwards
        for r in range(height - 2, -1, -1):
            # Iterate through each column
            for c in range(width):
                # Check if the current pixel is non-white (not 0)
                if output_grid[r, c] != 0:
                    # Check if the pixel directly below is white (0)
                    if output_grid[r + 1, c] == 0:
                        # Move the pixel down
                        output_grid[r + 1, c] = output_grid[r, c]
                        output_grid[r, c] = 0
                        moved = True  # Mark that a move occurred

        # If no pixels moved in this full pass, the grid is stable
        if not moved:
            break

    # Convert the NumPy array back to a list of lists before returning
    return output_grid.tolist()