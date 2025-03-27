import numpy as np

"""
Combine the left and right halves of the input grid based on pixel color presence.
The output grid has the same height as the input and half the width.
For each cell (r, c) in the output grid:
- If the corresponding cell in the left half of the input grid (input[r, c]) is non-white (not 0)
  OR the corresponding cell in the right half of the input grid (input[r, c + width/2]) is non-white (not 0),
  then the output cell (output[r, c]) is set to magenta (6).
- Otherwise (if both input cells are white (0)), the output cell (output[r, c]) is set to white (0).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Combines the left and right halves of an input grid based on pixel presence.

    Args:
        input_grid: A 2D numpy array representing the input grid.
                    It's assumed to have an even number of columns.

    Returns:
        A 2D numpy array representing the output grid, with the same height
        as the input and half the width.
    """
    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Calculate output dimensions
    output_height = input_height
    output_width = input_width // 2 # Integer division ensures correct width

    # Initialize the output grid with white (0) pixels
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the output grid
    for r in range(output_height):
        for c in range(output_width):
            # Get the corresponding pixel values from the left and right halves of the input grid
            left_pixel = input_grid[r, c]
            right_pixel = input_grid[r, c + output_width] # Offset by half the input width

            # Check if either the left or right pixel is non-white (not 0)
            if left_pixel != 0 or right_pixel != 0:
                # If either is non-white, set the output pixel to magenta (6)
                output_grid[r, c] = 6
            # Else: both pixels are white (0), so the output pixel remains white (0) as initialized

    return output_grid