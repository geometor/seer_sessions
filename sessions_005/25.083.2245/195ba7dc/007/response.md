```python
"""
Transforms an input grid into an output grid based on the presence of the digit '2' in each column. Columns with '2' are represented by a single column of all '1's in the output. Columns without '2' are processed row-wise: their non-zero elements are interleaved across rows, and are represented by '1's, while zeros are represented as '0's in the output grid.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_rows, input_cols = input_grid.shape

    # Separate columns into two groups: with '2' and without '2'
    cols_with_2_indices = []
    cols_without_2_indices = []
    for j in range(input_cols):
        if 2 in input_grid[:, j]:
            cols_with_2_indices.append(j)
        else:
            cols_without_2_indices.append(j)

    # Calculate output width for columns without '2' (row-wise interleaving)
    output_width_no_2 = 0
    for i in range(input_rows):
        for j in cols_without_2_indices:
            if input_grid[i, j] != 0:
                output_width_no_2 += 1

    # Initialize output grid
    output_cols = len(cols_with_2_indices) + output_width_no_2
    output_grid = np.zeros((input_rows, output_cols), dtype=int)

    # Fill output columns for input columns with '2'
    output_col_index = 0
    for j in cols_with_2_indices:
        output_grid[:, output_col_index] = 1
        output_col_index += 1

    # Fill output columns for input columns without '2' (row-wise interleaving)
    output_col_sub_index = 0
    for i in range(input_rows):
        for j in cols_without_2_indices:
            if input_grid[i, j] != 0:
                output_grid[i, output_col_index + output_col_sub_index] = 1
                output_col_sub_index += 1

    return output_grid.tolist()
```