"""
Iterates through each row of the input grid. If all values in a row are identical, the corresponding output row is all 5s. Otherwise, the corresponding output row is all 0s.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on whether all elements in a row are the same.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)  # Initialize output_grid with zeros

    # Iterate through each row of the input grid
    for i in range(input_grid.shape[0]):
        # Check if all elements in the current row are the same
        if np.all(input_grid[i] == input_grid[i, 0]):
            # If all elements are the same, replace the corresponding output row with 5s
            output_grid[i, :] = 5
        # else, output remains 0, as initialized.

    return output_grid.tolist()