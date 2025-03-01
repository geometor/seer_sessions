"""
1.  **Examine Column 4:** Inspect the fourth column (index 3) of the input grid.
2.  **Conditional Check:** Determine if *all* pixels in the fourth column are blue.
3.  **Output based on condition**:
    *   **If True (all blue):** Create output grid, same height as input, with every pixel in every column set to green. Set width of output to 3.
    *   **If False (not all blue):** Create output grid, same height as input with every pixel in every column set to white. Set width of output to 3.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same height as the input, and width 3.
    rows = len(input_grid)
    output_grid = np.zeros((rows, 3), dtype=int)

    # Extract the 4th column (index 3) from the input grid.
    check_column = input_grid[:, 3]

    # Check if all elements in the column are blue (1).
    if np.all(check_column == 1):
        output_grid[:] = 3  # Set all columns to green (3)
    else:
        output_grid[:] = 0 # Set all columns to white (0)

    return output_grid