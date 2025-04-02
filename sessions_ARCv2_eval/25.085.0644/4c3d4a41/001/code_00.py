import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on a stencil pattern.

    The grid is conceptually split into two halves: a left 'stencil' area and a
    right 'target' area. The transformation involves two main steps:
    1. Clearing the stencil area in the output grid to white (0).
    2. Modifying the target area in the output grid: If a pixel in the input grid's
       stencil area is gray (5), the corresponding pixel in the output grid's
       target area is set to gray (5). Otherwise, the target area pixel retains
       its original color from the input grid.
    """

    # Get grid dimensions
    height, width = input_grid.shape

    # Define the column index that splits the stencil and target areas
    # Based on observation, the right section starts at column 9 (0-indexed)
    split_col = 9

    # Initialize output_grid as a copy of the input_grid
    # This handles the pixels that don't change color based on the stencil
    output_grid = np.copy(input_grid)

    # 1. Clear the stencil area (left side) in the output grid to white (0)
    for r in range(height):
        for c in range(split_col):
            # Check if column index is within the stencil area boundaries
            if c < width: # Ensure we don't go out of bounds if width < split_col
                 output_grid[r, c] = 0

    # 2. Apply the stencil logic to the target area (right side)
    for r in range(height):
        # Iterate through columns in the target area
        for c in range(split_col, width):
            # Calculate the corresponding column index in the stencil area
            stencil_c = c - split_col

            # Check if the corresponding stencil pixel in the *input* grid is gray (5)
            if input_grid[r, stencil_c] == 5:
                # If it is gray, set the current target pixel in the *output* grid to gray (5)
                output_grid[r, c] = 5
            # Else (stencil pixel is not gray):
            # The output_grid pixel at [r, c] already holds the correct value
            # because it was copied from the input_grid initially. No action needed.

    return output_grid