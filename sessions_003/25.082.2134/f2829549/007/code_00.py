"""
1.  **Identify the Key Column:** Find the single column in the input grid that contains the value '1' (blue). This is the "key column".

2.  **Create Output Grid:** Create an output grid with the same number of rows as the input grid and a fixed width of 3 columns. All cells are initialized to '0' (white).

3.  **Process Each Row:** For each row in the input grid:
    *   **Check for '1' in Key Column:** Determine if the cell at the key column index in the current input row contains the value '1'.

    *   **If '1' IS present:**
        *   Set the output grid's corresponding row, middle column (index 1) to '3' (green).
        *   Check the *left neighbor*: If a left neighbor exists (i.e., we're not in the first column) AND the left neighbor's value is NOT '0', set the output grid's corresponding row, left column (index 0) to '3'.
        *   Check the *right neighbor*: If a right neighbor exists (i.e., we're not in the last column) AND the right neighbor's value is NOT '0', set the output grid's corresponding row, right column (index 2) to '3'.

    *   **If '1' is NOT present:**
        *   Check the *left neighbor*: If a left neighbor exists AND the left neighbor's value is NOT '0', set the output grid's corresponding row, left column (index 0) to '3'.
        *   Check the *right neighbor*: If a right neighbor exists AND the right neighbor's value is NOT '0', set the output grid's corresponding row, right column (index 2) to '3'.
4. Return the output grid.
"""

import numpy as np

def find_key_column(grid):
    # Find the column index that contains the value 1
    for j in range(grid.shape[1]):
        if 1 in grid[:, j]:
            return j
    return -1  # Should not happen if 1 is guaranteed

def transform(input_grid):
    # Initialize output_grid
    rows = input_grid.shape[0]
    cols = 3
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the key column
    key_column_index = find_key_column(input_grid)

    # Process each row
    for i in range(rows):
        # Check for '1' in key column
        if input_grid[i, key_column_index] == 1:
            # If '1' is present
            output_grid[i, 1] = 3  # Set middle column to '3'

            # Check left neighbor
            if key_column_index > 0 and input_grid[i, key_column_index - 1] != 0:
                output_grid[i, 0] = 3

            # Check right neighbor
            if key_column_index < input_grid.shape[1] - 1 and input_grid[i, key_column_index + 1] != 0:
                output_grid[i, 2] = 3
        else:
            # If '1' is NOT present
            # Check left neighbor
            if key_column_index > 0 and input_grid[i, key_column_index - 1] != 0:
                output_grid[i, 0] = 3

            # Check right neighbor
            if key_column_index < input_grid.shape[1] - 1 and input_grid[i, key_column_index + 1] != 0:
                output_grid[i, 2] = 3

    return output_grid