"""
1.  **Initialization:** Create an output grid with the same number of rows as the input grid and 4 columns.  All cells in the output grid are initially set to 0 (white).

2.  **Row Iteration:** For each row in the input grid:

    a. **Locate Yellow Pixel:** Find the *first* yellow pixel (value 4) in the current row. If no yellow pixel is found in a row, that row in the output grid remains all zeros.

    b. **Subgrid Extraction:** If a yellow pixel is found at column `c` in row `r`, extract a subgrid from the input grid.
        -   The subgrid always starts at row `r`
        -   The subgrid extends at most two columns to the *left* of the yellow pixel.
        -   The subgrid's width is determined by how close the yellow pixel is to the left edge of the input grid. The right edge of the subgrid is always one position left of the yellow pixel.
            -   If the yellow pixel is at the very left edge (column 0), the subgrid has a width of 0.
            -   If the yellow pixel is one column away from the left edge (column 1), the subgrid has a width of 1.
            -   If the yellow pixel is two or more columns away from the left edge, the subgrid has a width of 2.
        - The subgrid's height is *always* 1.

    c. **Subgrid Transposition:** If a valid subgrid (width > 0) was extracted, *transpose* the subgrid. This changes a 1xN subgrid to an Nx1 subgrid.

    d. **Subgrid Placement:** Place the transposed subgrid into the output grid.
       -   The transposed subgrid is placed starting at column 0 of the output grid.
       -   The subgrid is placed in the *same row* (`r`) as the yellow pixel in the input grid.

3.  **Output:** The final output grid is the result of the transformation.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows = len(input_grid)
    cols = 4
    output_grid = np.zeros((rows, cols), dtype=int)

    # iterate through rows
    for r in range(rows):
        # locate yellow pixel
        yellow_col = -1
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 4:
                yellow_col = c
                break

        # subgrid extraction
        if yellow_col != -1:  # Ensure yellow pixel was found
            sub_r_start = r
            sub_c_start = max(0, yellow_col - 2) # at most 2 columns to the left
            sub_r_end = r + 1 # Only one row
            sub_c_end = yellow_col

            # extract the subgrid
            subgrid = input_grid[sub_r_start:sub_r_end, sub_c_start:sub_c_end]

            # subgrid transposition and placement
            if subgrid.size > 0:  # Ensure subgrid is not empty
                transposed_subgrid = subgrid.T  # Always transpose

                # Place the subgrid
                output_grid[r:r + transposed_subgrid.shape[0], 0:transposed_subgrid.shape[1]] = transposed_subgrid

    return output_grid