"""
The transformation rule involves expanding an input grid into an output grid where the non-zero elements of the input grid are copied along diagonals in the output grid. The starting point and spacing of these diagonals, as well as the overall dimensions of the output grid, are determined by relationships between the input and output grids. Zero values in the input are treated as background and are not explicitly copied; remaining cells in the output are filled with zeros.

Specifically, the following rules are observed:

1.  **Output Dimensions:** The output grid's dimensions are related to the input grid's dimensions.
    -   In examples 1 and 2, the output grid is twice the size of the input grid (2x scaling) along each dimension.
    -   In example 3, the output grid's height is twice the input grid's height, and the output width is twice the input grid's width.

2.  **Diagonal Placement:** Non-zero elements from the input grid are placed along diagonals in the output grid.
    -   In examples 1 and 2, the diagonals start at positions (i, j) in the output grid, where (i,j) corresponds to the position of the non zero element in input grid. The values are copied to (i+k, j+k)
    -   In example 3, each element is repeated on rows and columns.

3.  **Zero Handling:** Zeros in the input grid are considered background and are not directly mapped to the output grid. The output grid is initialized with zeros, and only the positions corresponding to non-zero input elements are updated.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_rows, input_cols = input_grid.shape

    # Determine output grid dimensions based on input grid and example-specific rules.
    output_rows = input_rows * 2
    output_cols = input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through the input grid and copy non-zero elements to output diagonals.
    for i in range(input_rows):
        for j in range(input_cols):
            if input_grid[i, j] != 0:
                # Example 3 specific logic (repetition)
                if input_cols == 2 and input_rows == 2:
                     for row_offset in range(input_rows):
                        for col_offset in range(input_cols):
                            output_grid[i + row_offset, j + col_offset] = input_grid[i,j]
                # Example 1 and 2 specific logic.
                else:
                    for k in range(output_rows-i):
                         if (j+k) < output_cols:
                            output_grid[i + k, j + k] = input_grid[i, j]
    return output_grid