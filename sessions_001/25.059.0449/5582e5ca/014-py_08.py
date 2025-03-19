"""
The transformation rule is a conditional statement based on the presence of the digit '9' (maroon color) within the input grid.

1.  **Check for '9':** Examine the input grid to determine if the value '9' is present anywhere within the grid.

2.  **Conditional Output:**
    *   **If '9' is present:** Create a new output grid that has the *exact same dimensions* (height and width) as the input grid. Fill every cell of this output grid with the value '9'.
    *   **If '9' is not present:** Create a new output grid that has the *exact same dimensions* as the input grid. Fill every cell of this output grid with the value '0'.

The core logic is a simple presence check followed by a complete replacement of the grid content based on that check, while preserving the original grid's dimensions.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence of the digit '9'.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed output grid.
    """
    # Check if the value '9' is present in the input grid.
    if 9 in input_grid:
        # If '9' is present, create an output grid of the same dimensions filled with '9'.
        output_grid = np.full(input_grid.shape, 9, dtype=int)
    else:
        # If '9' is not present, create an output grid of the same dimensions filled with '0'.
        output_grid = np.full(input_grid.shape, 0, dtype=int)

    return output_grid