"""
1.  **Find Center:** Locate the central vertical column of the input grid (index = width // 2).
2.  **Extract Subgrid:** Extract a 3-column-wide subgrid centered on the identified central column. This means taking the central column itself, one column to its left, and one column to its right, while keeping all rows.
3.  **Conditional Recolor:** For each row in the subgrid, if the output pixel is different from the input pixel, then it is replaced by the value of the other non-center pixel. If there is a change to a pixel in the left or right of the extracted subgrid, change to the color of the opposite side.
4.  **Output:** The resulting 3xN subgrid (where N is the number of rows) is the output.
"""

import numpy as np

def get_central_column_index(grid):
    """Helper function to find the index of the central column."""
    return grid.shape[1] // 2

def extract_subgrid(grid, center_col_index, width):
    """Helper function to extract a subgrid of specified width centered on a column."""
    start_col = max(0, center_col_index - width // 2)
    end_col = min(grid.shape[1], center_col_index + width // 2 + 1)
    return grid[:, start_col:end_col]


def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Locate Center
    center_col_index = get_central_column_index(input_grid)

    # 2. Extract Subgrid
    subgrid = extract_subgrid(input_grid, center_col_index, 3)
    output_grid = subgrid.copy()

    # 3. Conditional Recolor
    center_sub = subgrid.shape[1] // 2
    for i in range(subgrid.shape[0]):
        # Check left neighbor
        if subgrid[i, center_sub -1] != output_grid[i, center_sub-1] :
          output_grid[i, center_sub - 1] = subgrid[i, center_sub+1]

        # Check right neighbor
        if subgrid[i, center_sub + 1] != output_grid[i, center_sub + 1]:
            output_grid[i, center_sub+1] = subgrid[i, center_sub-1]
        
        #center neighbor
        if subgrid[i, center_sub] != output_grid[i, center_sub] and subgrid[i, center_sub]==1:
          output_grid[i, center_sub]=8
    # 4. Output
    return output_grid.tolist()