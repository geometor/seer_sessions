"""
1.  **Input:** A 3x3 grid of colored pixels.
2.  **Output:** A 6x6 grid of colored pixels (double the dimensions).
3.  **Transformation:**
    *   Create a 6x6 output grid filled with zeros (black).
    *   Iterate through each cell of the input grid using row and column indices (i, j).
    *   For each cell (i, j) in the input grid:
        *   Copy the value of the input cell to the output grid, starting at position (i, j).
        *   Continue copying the input cell's value diagonally down and to the right in the output grid: (i+1, j+1), (i+2, j+2), and so on, until reaching the output grid's boundaries.

    *   The first input element (0,0) begins its diagonal replication at (0,0)

    *   For the next element in the first row (0,1) the diagonal replication also
        starts from it's offset position in the output (0, 1), and replicates as
        (0, 1) -> (1, 2) -> (2, 3)
    *   The element on the second row (1, 0), will go as
        (1, 0), (2, 1), (3, 2)

    *   So, input[i][j] will be copied at all output locations [i+k][j+k] until
        it reaches output boundaries.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows * 2
    output_cols = input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through the input grid
    for i in range(input_rows):
        for j in range(input_cols):
            # Copy the value diagonally
            for k in range(min(output_rows - i, output_cols - j)):
                output_grid[i + k, j + k] = input_grid[i, j]

    return output_grid