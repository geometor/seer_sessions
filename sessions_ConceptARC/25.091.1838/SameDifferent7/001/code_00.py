import numpy as np

"""
Identify pixels in the input grid that are completely surrounded by non-white pixels.
Specifically, a pixel is kept if and only if it and all of its 8 immediate neighbors (including diagonals) are non-white (not color 0). 
All other pixels are set to white (0) in the output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by keeping only pixels that are fully surrounded by non-white pixels.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Iterate through each pixel of the input grid, excluding the border pixels
    # Border pixels cannot be fully surrounded by 8 neighbors within the grid.
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check if the current pixel itself is non-white
            if input_grid[r, c] == 0:
                continue # Skip if the center pixel is white

            # Extract the 3x3 neighborhood around the current pixel
            neighborhood = input_grid[r-1 : r+2, c-1 : c+2]

            # Check if *all* pixels in the 3x3 neighborhood are non-white (not 0)
            # np.all returns True if all elements evaluate to True (non-zero in this context)
            if np.all(neighborhood != 0):
                # If all neighbors (and the center) are non-white,
                # copy the color of the current pixel to the output grid
                output_grid[r, c] = input_grid[r, c]

    # Return the resulting output grid
    return output_grid