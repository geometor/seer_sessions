"""
1.  **Initialization:** Create an output grid with the same number of rows as the input grid and 4 columns. All cells are initially set to 0.
2.  **Row Iteration:** For each row in the input grid:
    a. **Locate Yellow Pixel:** Find the yellow pixel (value 4) in the current row.
    b. **Subgrid Extraction:** Extract a subgrid from the input grid based on the yellow pixel's location.
        - The yellow pixel's column dictates the extraction logic. We want to extract the two columns to its left.
        - Ideally, extract a 2x2 subgrid. The yellow pixel's location serves as a guide (conceptually the lower-right corner of the 2x2 area).
        - If a 2x2 subgrid cannot be formed because the yellow pixel is too close to the edges (top, bottom, or left side):
            - If the yellow pixel is one from the top edge, take one row below.
            - If the yellow pixel is at the very left edge, the subgrid width will be 0 and we won't be able extract anything to the left of it, and thus no valid subgrid is produced.
            -If the yellow pixel is one away from the left edge, we extract only one column on the left side.
    c. **Subgrid Rotation:** If a valid subgrid (of any dimensions) was extracted: rotate it by 180 degrees if it is 2x2, or transpose if not. If a 2x0 subgrid exists, do not rotate or place.
    d. **Subgrid Placement:** Place the rotated subgrid (or the original, if it was not 2x2) into the output grid. The placed subgrid starts at column 0 of the output grid and occupies the same row(s) as the current row being processed in the input grid.
3.  **Output:** The final output grid is the result of this transformation.
"""

import numpy as np

def rotate_180(subgrid):
    """Rotates a 2x2 subgrid by 180 degrees."""
    return np.rot90(subgrid, 2)

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
            sub_r_end = min(rows, r + 2)
            sub_c_end = yellow_col

            # extract the subgrid with corrected bounds, handling edge cases directly.
            subgrid = input_grid[sub_r_start:sub_r_end, sub_c_start:sub_c_end]

            # subgrid rotation and placement
            if subgrid.size > 0:  # Ensure subgrid is not empty
                if subgrid.shape == (2, 2):
                    rotated_subgrid = rotate_180(subgrid)
                else:
                    rotated_subgrid = subgrid.T  # Transpose for non-square subgrids

                # Place the subgrid correctly.  The subgrid's *rotated* dimensions
                # determine how much of the output grid to fill
                output_grid[sub_r_start:sub_r_start + rotated_subgrid.shape[0], 0:rotated_subgrid.shape[1]] = rotated_subgrid

    return output_grid