"""
Identify all pixels in the input grid that are not white (color 0).
Count the total number (N) of these non-white pixels.
Create a new output grid with 1 row and N columns.
Iterate through the input grid, scanning row by row from top to bottom, and within each row, scanning column by column from left to right.
For each non-white pixel encountered during the scan, place its color into the next available column in the output grid, starting from the leftmost column (index 0).
The final output grid contains all the non-white pixels from the input, arranged horizontally in the order they were found.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting non-background pixels and arranging them in a single row.

    Args:
        input_grid (list or np.array): A 2D grid representing the input.

    Returns:
        np.array: A 1D numpy array containing the non-background pixels from the input grid,
                  in the order they were encountered during a row-major scan.
    """
    # Convert input to numpy array for easier handling
    input_grid_np = np.array(input_grid)

    # Find the dimensions of the input grid
    height, width = input_grid_np.shape

    # Initialize a list to store the non-white pixels
    non_white_pixels = []

    # Iterate through the input grid row by row, then column by column
    for r in range(height):
        for c in range(width):
            pixel_value = input_grid_np[r, c]
            # Check if the pixel is not white (0)
            if pixel_value != 0:
                non_white_pixels.append(pixel_value)

    # If no non-white pixels are found, return an empty array or handle as needed
    # Based on examples, if there are non-white pixels, the output is never empty.
    # The case of an all-white input isn't shown, but returning an empty 1D array seems logical.
    if not non_white_pixels:
        return np.array([[]]) # Or perhaps np.array([]) depending on expected format for empty

    # Create the output grid as a 1D numpy array (1 row, N columns)
    output_grid = np.array([non_white_pixels])

    return output_grid
