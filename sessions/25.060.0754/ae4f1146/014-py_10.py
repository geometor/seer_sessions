"""
The transformation rule can be described as follows:

1.  **Divide:** Divide the 9x9 input grid into nine 3x3 non-overlapping subgrids.
2.  **Reduce:** For each 3x3 subgrid:
    *   Iterate through the pixels in the subgrid.
    *   If all pixels are 0 (white), the corresponding output pixel is 0 (white).
    *   If there are any non-zero pixels, the output pixel takes the value of the *first* non-zero color encountered in the subgrid, when iterating from left-to-right and top-to-bottom.
3.  **Output:** The result of each subgrid's reduction forms a single pixel in the 3x3 output grid. The output grid's pixels are arranged in the same layout as the subgrids within the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_array = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the 3x3 subgrids
    for i in range(3):
        for j in range(3):
            # Extract the 3x3 subgrid
            subgrid = input_array[i*3:(i+1)*3, j*3:(j+1)*3]

            # Apply the reduction rule
            unique_colors = np.unique(subgrid)
            non_zero_colors = unique_colors[unique_colors != 0]

            if len(non_zero_colors) > 0:
                output_grid[i, j] = non_zero_colors[0]
            # else the default 0 is correct

    return output_grid.tolist()