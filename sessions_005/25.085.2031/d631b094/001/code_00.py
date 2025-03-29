"""
Scan the input grid row by row, top to bottom, then left to right within each row.
Collect all non-white pixels (color > 0) in the order they are encountered.
Create a 1xN output grid, where N is the count of non-white pixels found.
Populate this output grid with the collected non-white pixel colors.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts non-white pixels from the input grid and arranges them
    horizontally in a single row.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: A 1xN grid containing the non-white pixels.
    """
    # Convert input list of lists to a numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)

    # Find the indices of non-white pixels (where value > 0)
    # np.where returns indices row by row, then column by column, matching the required scan order
    non_white_indices = np.where(grid > 0)

    # Extract the values (colors) of the non-white pixels using the found indices
    # The order of values extracted corresponds to the row-major scan order
    non_white_pixels = grid[non_white_indices]

    # If no non-white pixels are found, return an empty array or handle as appropriate
    # Based on examples, there's always at least one non-white pixel
    # if non_white_pixels.size == 0:
    #     return np.array([[]], dtype=int) # Or perhaps np.empty((1, 0), dtype=int)

    # Create the output grid as a 1D array (which represents a single row)
    # Reshape it explicitly to be a 2D array with 1 row
    output_grid = non_white_pixels.reshape(1, -1)

    return output_grid
