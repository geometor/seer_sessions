import numpy as np
import copy

# Define the target 3x3 patterns composed of blue (1) and white (0) pixels.
# Patterns that should be changed to orange (7)
PATTERNS_TO_ORANGE = [
    np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]]), # X shape
    np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]), # Filled Square
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]), # Plus shape
    np.array([[1, 0, 1], [1, 0, 1], [1, 1, 1]]), # U shape
]

# Patterns that should be changed to azure (8)
PATTERNS_TO_AZURE = [
    np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]), # Square/O shape
    np.array([[1, 0, 1], [1, 1, 1], [1, 0, 1]]), # H shape
    np.array([[1, 1, 1], [1, 0, 0], [1, 1, 1]]), # C shape
]

"""
Identifies specific 3x3 patterns composed solely of blue (1) and white (0) pixels 
in the input grid. 
Based on the shape of the blue pattern, it is replaced with either orange (7) 
or azure (8) pixels in the corresponding locations, while white pixels remain white.
Patterns containing any color other than blue or white are ignored.

Specifically:
- 'X', 'Filled Square', 'Plus', and 'U' shapes made of blue pixels are converted to orange.
- 'Square/O', 'H', and 'C' shapes made of blue pixels are converted to azure.
"""

def transform(input_grid):
    """
    Transforms the input grid based on identifying and replacing specific 3x3 blue patterns.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = copy.deepcopy(input_np)
    height, width = input_np.shape

    # Iterate through all possible top-left corners (r, c) of 3x3 subgrids
    for r in range(height - 2):
        for c in range(width - 2):
            # Extract the 3x3 subgrid
            subgrid = input_np[r:r+3, c:c+3]

            # Check if the subgrid contains only blue (1) and white (0) pixels
            # And ensure it actually contains at least one blue pixel (is not all white)
            is_blue_white_only = np.all(np.isin(subgrid, [0, 1]))
            has_blue = np.any(subgrid == 1)

            if is_blue_white_only and has_blue:
                # Flag to check if pattern was found and processed
                pattern_found = False

                # Check if the subgrid matches any pattern designated for orange (7)
                for pattern in PATTERNS_TO_ORANGE:
                    if np.array_equal(subgrid, pattern):
                        # Apply the transformation: blue (1) becomes orange (7)
                        for i in range(3):
                            for j in range(3):
                                if subgrid[i, j] == 1:
                                    output_grid[r + i, c + j] = 7
                        pattern_found = True
                        break # Stop checking orange patterns once matched

                # If not found in orange patterns, check azure patterns
                if not pattern_found:
                    for pattern in PATTERNS_TO_AZURE:
                        if np.array_equal(subgrid, pattern):
                            # Apply the transformation: blue (1) becomes azure (8)
                            for i in range(3):
                                for j in range(3):
                                    if subgrid[i, j] == 1:
                                        output_grid[r + i, c + j] = 8
                            # pattern_found = True # No need to set flag again, just break
                            break # Stop checking azure patterns once matched

    # Convert back to list of lists for the required output format
    return output_grid.tolist()