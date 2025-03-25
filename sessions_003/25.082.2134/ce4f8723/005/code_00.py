"""
1.  **Initialization:** The `output_grid` has the same dimensions as `input_grid_1`.
2.  **Transformation Rule:** Iterate through each cell position (r, c) of both input grids.
    *   If the value of `input_grid_2` at (r, c) is 4, 2, or 0, *and* the value of `input_grid_1` at (r,c) is different than 3: change the corresponding cell in the `output_grid` at (r, c) to 3 (green).
    * Otherwise the value at (r,c) in `output_grid` takes the value of `input_grid_1` at (r,c).
3.  **Output:** The `output_grid` is the result of the transformation.
"""

import numpy as np

def transform(inputs):
    input_grid_1 = np.array(inputs[0])
    input_grid_2 = np.array(inputs[1])

    # Initialize output_grid with the same values as input_grid_1
    output_grid = np.copy(input_grid_1)

    # Iterate through each cell
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            # Check if within bounds of input_grid_2
            if r < input_grid_2.shape[0] and c < input_grid_2.shape[1]:
                # Apply the transformation rule
                if input_grid_2[r, c] in (4, 2, 0) and input_grid_1[r,c] != 3:
                    output_grid[r, c] = 3

    return output_grid.tolist()