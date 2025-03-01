"""
1.  **Grid Expansion:** The input grid is expanded into an output grid. The output grid's width is three times the input grid's width, and the output grid's height is two times the input grid's height plus one.

2.  **Row-wise Pattern Replication:** For each row in the input grid, a three-row pattern is created in the output grid.

3.  **First Row:** The first row of the pattern consists of the corresponding input pixel from the input row, followed by a 0 (white), followed by an 8 (azure). This sequence (input pixel, 0, 8) repeats across the entire width of the output row.

4.  **Second Row:** The second row of the pattern is filled entirely with 0s (white).

5.  **Third Row:** The third row of the pattern consists of the repeating sequence "8, 0, 8" (azure, white, azure) across the entire width of the output row.

6. **Iterate:** Steps 3-5 are repeated for every row of the original input grid. The three-row patterns are stacked vertically in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2 + 1, input_cols * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # change output pixels 
    for i in range(input_rows):
        # First row of the pattern
        for j in range(input_cols):
            output_grid[i * 2, j * 3] = input_grid[i, j]
            output_grid[i * 2, j * 3 + 1] = 0
            output_grid[i * 2, j * 3 + 2] = 8

        # Second row of the pattern
        output_grid[i * 2 + 1, :] = 0

        # Third row of the pattern
        if i*2+2 < output_rows: # making sure not to exceed boundaries
            for j in range(output_cols):
                output_grid[i * 2 + 2, j] = 8 if (j % 3 != 1) else 0
    return output_grid