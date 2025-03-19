"""
1.  **Identify Target Pixels:** Focus on the first column (excluding the top-left pixel) and the second element of the first row.
2.  **Conditional Swap 1:** If the pixel at `grid[1, 0]` (second row, first column) is different in color/value from the pixel at `grid[0, 1]` (first row, second column), they are swapped.
3. **Conditional Swap 2:** The pixel at `grid[2, 0]` is considered.
    * If the value of pixel at `grid[2, 0]` is different than `grid[1,0]` and has the *same* color/value as `grid[0, 1]`, then `grid[2, 0]` swaps with `grid[1, 0]`.
    * If the value of pixel at `grid[2,0]` is the same as `grid[1,0]`, then `grid[2,0]` swaps with `grid[0,1]`.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    # Conditional Swap 1:
    if output_grid[1, 0] != output_grid[0, 1]:
        output_grid[1, 0], output_grid[0, 1] = output_grid[0, 1], output_grid[1, 0]

    # Conditional Swap 2:
    if output_grid[2, 0] != output_grid[1, 0] and output_grid[2, 0] == output_grid[0, 1]:
        output_grid[2, 0], output_grid[1, 0] = output_grid[1, 0], output_grid[2, 0]
    elif output_grid[2,0] == output_grid[1,0]:
        output_grid[2, 0], output_grid[0, 1] = output_grid[0, 1], output_grid[2, 0]


    return output_grid