"""
Transforms a 2x13 grid of pixels based on the color and position of each pixel.

White (0) pixels remain white (0).
Blue (1) pixels change color based on their grid coordinates (row r, column c):
- If the pixel is in the first row (r=0) and its column index c is between 2 and 7 (inclusive), it becomes azure (8).
- Otherwise (if the pixel is blue but not in the specified section of the first row), it becomes gray (5).
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A numpy array representing the 2x13 input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Initialize output_grid by copying the input grid.
    # This handles the case where white (0) pixels stay white (0) by default.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Get the value of the current pixel
            pixel_value = input_grid[r, c]

            # Check if the pixel is blue (1)
            if pixel_value == 1:
                # Apply the conditional rule based on position
                if r == 0 and 2 <= c <= 7:
                    # Change to azure (8) if in the specific zone of the first row
                    output_grid[r, c] = 8
                else:
                    # Change to gray (5) for all other blue pixels
                    output_grid[r, c] = 5
            # No explicit action needed for pixel_value == 0, as it was copied initially.
            # You could add handling for other unexpected pixel values if necessary.

    return output_grid