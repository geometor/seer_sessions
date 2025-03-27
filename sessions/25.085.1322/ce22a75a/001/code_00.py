"""
Transforms an input grid by replacing each gray pixel (5) with a 3x3 square of blue pixels (1) centered at the original gray pixel's location. Overlapping blue squares merge.
"""

import numpy as np

def transform(input_grid):
    """
    Replaces each gray pixel in the input grid with a 3x3 blue square in the output grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize output_grid with the same dimensions as input_grid, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell contains a gray pixel (5)
            if input_grid[r, c] == 5:
                # Define the 3x3 region centered at (r, c)
                # Iterate through the rows of the 3x3 square
                for dr in range(-1, 2):
                    # Iterate through the columns of the 3x3 square
                    for dc in range(-1, 2):
                        # Calculate the coordinates in the output grid
                        nr, nc = r + dr, c + dc
                        # Check if the coordinates are within the grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            # Change the color of the cell to blue (1)
                            output_grid[nr, nc] = 1

    # Return the final output grid
    return output_grid