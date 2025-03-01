"""
The transformation extracts a 4x4 subgrid from the input grid. The first three columns of the output grid
correspond to the first three columns of the input grid. The fourth column's values are derived based on the
presence and arrangement of colors within specific rows of the input grid.

1.  **Subgrid Extraction:** The output is a 4x4 subgrid of the input grid.
2.  **Column Copy:** The first three columns of the output grid are identical to the first three columns of the input grid (index 0-2).
3.  **Fourth Column Derivation:**
    *   The value of the first row (row 0) in the fourth column is always 1.
    *   The rest of the values are derived as follows:
        * If the row contains only colors matching the color of the input at (1,1), then output the color from input(1,1).
        * If the row contains mixed colors, but at least one pixel matching input(1,1), output 5.
        *  If the row is a solid color, and does NOT match input(1,1), output 0.

"""

import numpy as np

def transform(input_grid):
    """
    Extracts a 4x4 subgrid, copies the first 3 columns, and derives the 4th column.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((4, 4), dtype=int)

    # Copy the first three columns
    output_grid[:, :3] = input_grid[:4, :3]

    # Derive the fourth column
    output_grid[0, 3] = 1  # First row is always 1

    target_color = input_grid[1, 1]

    for i in range(1, 4):
        row_colors = set(input_grid[i,:])
        if len(row_colors) == 1:  # solid color
            if input_grid[i,0] == target_color:
              output_grid[i,3] = target_color
            else:
              output_grid[i,3] = 0

        elif target_color in row_colors: # mixed with target color
            output_grid[i, 3] = 5

        elif len(row_colors) > 1:
            row_colors_list = list(input_grid[i,:])
            if target_color in row_colors_list:
               output_grid[i,3] = 5
            else:
               output_grid[i,3] = 0

    return output_grid.tolist()