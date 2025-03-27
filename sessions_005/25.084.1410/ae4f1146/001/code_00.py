"""
Iterate through all possible 3x3 subgrids within the input grid.
Identify candidate subgrids that meet three criteria:
1. Contain no white (0) pixels.
2. Contain at least one blue (1) pixel.
3. Contain at least one azure (8) pixel.
From the candidate subgrids, select the one with the maximum count of blue (1) pixels.
Return this selected 3x3 subgrid as the output.
"""

import numpy as np

def transform(input_grid):
    """
    Finds a 3x3 subgrid within the input grid that contains no white pixels,
    at least one blue and one azure pixel, and maximizes the count of blue pixels.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: The 3x3 output subgrid, or None if no suitable subgrid is found.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    best_subgrid = None
    max_blue_count = -1

    # Define the size of the subgrid
    subgrid_size = 3

    # Iterate through all possible top-left corners (r, c) of a 3x3 subgrid
    for r in range(height - subgrid_size + 1):
        for c in range(width - subgrid_size + 1):
            # Extract the 3x3 subgrid
            subgrid = input_grid[r:r + subgrid_size, c:c + subgrid_size]

            # Check filtering criteria:
            # 1. No white (0) pixels
            contains_white = np.any(subgrid == 0)
            if contains_white:
                continue  # Skip this subgrid if it contains white

            # 2. At least one blue (1) pixel
            contains_blue = np.any(subgrid == 1)
            if not contains_blue:
                continue # Skip this subgrid if it doesn't contain blue

            # 3. At least one azure (8) pixel
            contains_azure = np.any(subgrid == 8)
            if not contains_azure:
                continue # Skip this subgrid if it doesn't contain azure

            # If all criteria met, this is a candidate subgrid
            # Calculate the count of blue pixels in this candidate
            current_blue_count = np.sum(subgrid == 1)

            # Compare with the best candidate found so far
            if current_blue_count > max_blue_count:
                max_blue_count = current_blue_count
                best_subgrid = subgrid

    # Return the best subgrid found
    # Convert back to list of lists if necessary for ARC environment,
    # but numpy array is often preferred for internal processing.
    # If best_subgrid is still None, it means no suitable subgrid was found.
    return best_subgrid.tolist() if best_subgrid is not None else None
