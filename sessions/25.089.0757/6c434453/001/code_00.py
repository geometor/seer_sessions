"""
Transformation Rule:
Find all occurrences of a specific 3x3 pattern within the input grid and replace them with another specific 3x3 pattern.

The target pattern is a 3x3 hollow square made of blue (1) pixels surrounding a white (0) center:
[[1, 1, 1],
 [1, 0, 1],
 [1, 1, 1]]

The replacement pattern is a 3x3 plus sign made of red (2) pixels on a white (0) background:
[[0, 2, 0],
 [2, 2, 2],
 [0, 2, 0]]

Pixels in the grid not part of any matched target pattern remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the pattern replacement transformation to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier slicing and comparison
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input grid
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Define the target pattern (hollow blue square)
    target_pattern = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ], dtype=int)

    # Define the replacement pattern (red plus sign)
    replacement_pattern = np.array([
        [0, 2, 0],
        [2, 2, 2],
        [0, 2, 0]
    ], dtype=int)

    # Iterate through all possible top-left corners (r, c) for a 3x3 subgrid
    # The loops stop at height-2 and width-2 because we need a full 3x3 area
    for r in range(height - 2):
        for c in range(width - 2):
            # Extract the 3x3 subgrid from the input grid starting at (r, c)
            subgrid = input_np[r:r+3, c:c+3]

            # Compare the extracted subgrid with the target pattern
            if np.array_equal(subgrid, target_pattern):
                # If they match, replace the corresponding area in the output grid
                # with the replacement pattern
                output_np[r:r+3, c:c+3] = replacement_pattern

    # Convert the final NumPy array back to a list of lists before returning
    return output_np.tolist()