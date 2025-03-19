"""
1.  **Identify the Main Diagonal:** Find the elements located at positions (i, i) where the row index `i` equals the column index `i`.
2.  **Row Filling:** For *each* row in the grid, replace *all* elements in that row with the value of the element found on the main diagonal at the *same row index*. In other words. `output[i][j] = input[i][i]` for all `j`.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the initial output
    output_grid = np.copy(input_grid)
    rows = len(output_grid)
    cols = len(output_grid[0])

    # Iterate through each row
    for i in range(rows):
        # Get the value of the diagonal element for this row
        diagonal_value = input_grid[i][i]
        # Fill the entire row with the diagonal value
        for j in range(cols):
            output_grid[i][j] = diagonal_value

    return output_grid