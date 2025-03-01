"""
1. Identify All-Zero Columns: Examine each column in the input grid. If *all* pixels in a column have a value of 0 (white), then that column is marked for transformation.
2. Apply Transformation:  *All* pixels in the columns identified in step 1 are changed to the color magenta (6).
3. No other changes: If a column has even a single pixel that is *not* 0, that entire column in the input is left completely unchanged in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all-zero columns with magenta.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array
    input_grid_np = np.array(input_grid)

    # Get dimensions
    num_rows, num_cols = input_grid_np.shape

    # Create a copy for the output
    output_grid_np = np.copy(input_grid_np)

    # Iterate through columns
    for j in range(num_cols):
        # Check if the column is all zeros
        if np.all(input_grid_np[:, j] == 0):
            # Replace the entire column with magenta (6)
            output_grid_np[:, j] = 6

    # Convert back to list of lists
    output_grid = output_grid_np.tolist()
    return output_grid