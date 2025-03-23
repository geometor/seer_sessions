"""
1.  **Identify Repeating Sub-Patterns:** Scan the input grid and identify the smallest repeating rectangular sub-pattern that, when tiled, completely covers the input grid.  The sub-pattern can be 1xN, Nx1 or NxN.

2.  **Extract Top-Left Instance:** Extract the top-left instance of this repeating sub-pattern.

3.  **Output:** The extracted sub-pattern becomes the output grid.
"""

import numpy as np

def find_repeating_subpattern(grid):
    rows, cols = grid.shape
    for sub_rows in range(1, rows + 1):
        for sub_cols in range(1, cols + 1):
            if rows % sub_rows == 0 and cols % sub_cols == 0:
                sub_pattern = grid[0:sub_rows, 0:sub_cols]
                valid_pattern = True
                for i in range(0, rows, sub_rows):
                    for j in range(0, cols, sub_cols):
                        if not np.array_equal(grid[i:i+sub_rows, j:j+sub_cols], sub_pattern):
                            valid_pattern = False
                            break
                    if not valid_pattern:
                        break
                if valid_pattern:
                    return sub_pattern
    return grid  # Should never reach here in theory, but return input if no pattern is found

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Find the repeating sub-pattern.
    sub_pattern = find_repeating_subpattern(input_grid)

    # The sub-pattern is the output.
    output_grid = sub_pattern

    return output_grid.tolist()