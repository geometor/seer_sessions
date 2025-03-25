"""
1.  **Identify First '2':** Find the first occurrence of the digit '2' (red color) in the input grid. Note its column index.
2.  **Select Rows:** The output grid always consists of the first 4 rows of the input grid.
3.  **Select Columns:** Output grid always contains 4 last columns based on the last values in the first 4 rows.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((4, 4), dtype=int)

    # Select the first 4 rows.
    for i in range(min(4, rows)):
        # get last four columns
        for j in range(min(4, cols)):
            output_grid[i,j] = input_grid[i, cols - 4 + j]
    
    return output_grid.tolist()