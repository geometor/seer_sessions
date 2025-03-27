"""
1.  **Input:** A 3x3 grid (2D array) of colored pixels, where each color is represented by an integer (0-9).
2.  **Output:** A 6x6 grid (2D array) of colored pixels. The output grid's dimensions are double the input grid's dimensions.
3.  **Transformation:**
    *   Create an output grid filled with zeros (black).
    *   Iterate through each cell of the input grid using row and column indices (i, j).
    *   For each cell (i, j) in the input grid, copy its value to the output grid starting at the position (i, j).
    *   From this starting position (i, j), continue copying the same input cell value diagonally down and to the right in the output grid. That is, copy to positions (i+1, j+1), (i+2, j+2), and so on, until the boundaries of the output grid are reached.
    * For the next row in the input (i+1, j) the copy starts at (i + 1, j)
    *   The result is that each row of the input grid seeds a diagonal replication, and each successive input row's replication starts one column further to the right.
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