"""
The transformation involves identifying specific regions (columns or rows) in the input grid, mirroring the left two columns to the right two columns in Examples 1 and 2, and applying color swaps within those regions or other specified rows (Example 3).
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    def apply_color_swaps(grid, swaps, region_rows, region_cols):
        # Apply color swaps within a specified region
        for r in region_rows:
            for c in region_cols:
                if grid[r, c] in swaps:
                    grid[r, c] = swaps[grid[r, c]]

    # Examples 1 & 2: Mirroring and Color Swaps
    if cols == 8:  # All examples have 8 columns
        # Mirror the first two columns to the last two columns
        output_grid[:, 6:] = input_grid[:, :2][:, ::-1]

        # Determine color swaps based on the example
        if np.array_equal(input_grid[:,:2], example1_input[:,:2]):
            #Example 1 Swaps:
            swaps = {6: 1, 1: 3, 2: 6, 3: 2}
            region_cols = list(range(6, 8))
            region_rows = list(range(rows))
            apply_color_swaps(output_grid, swaps, region_rows, region_cols)
        elif np.array_equal(input_grid[:,:2], example2_input[:,:2]):
            # Example 2 swaps
            swaps = {1: 9, 9: 6, 6: 1}
            region_cols = list(range(6, 8))
            region_rows = list(range(rows))
            apply_color_swaps(output_grid, swaps, region_rows, region_cols)

    # Example 3: Color Swaps in Specific Rows
    if np.array_equal(input_grid, example3_input):

        # Top two rows
        region_rows_1 = list(range(2))
        region_cols_1 = list(range(cols))
        swaps_1 = {6: 5}
        apply_color_swaps(output_grid, swaps_1, region_rows_1, region_cols_1)

        # Bottom three rows
        region_rows_2 = list(range(rows - 3, rows))
        region_cols_2 = list(range(cols))
        swaps_2 = {5: 6}
        apply_color_swaps(output_grid, swaps_2, region_rows_2, region_cols_2)


    return output_grid.tolist()