"""
1.  **Examine** each row in the input grid.
2.  **Identify** rows that contain only black pixels (black rows) and rows that contain at least one non-black pixel (non-black rows).
3.  **Store** the non-black rows in a separate list.
4.  **Reverse** the order of the list of non-black rows.
5.  **Construct** the output grid as follows.
6.  **Iterate** through the *indices* of the input grid's rows.
    - Add to the output, rows of all black pixels at the same index where they occur in the input.
    - After placing all the original black lines, append the reversed non-black rows to the *end* of the output.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    non_black_rows = []
    black_rows_indices = []

    # 1. & 2. Identify and separate row types
    for i, row in enumerate(input_grid):
        if np.all(row == 0):
            black_rows_indices.append(i)
        else:
            non_black_rows.append(row)

    # 3. Reverse Non-Black Rows
    non_black_rows.reverse()

    # 4. Construct Output
    output_grid = []

    # 5. Add original black rows using index
    for i in black_rows_indices:
        output_grid.append(input_grid[i])

    # 6. Append reversed non-black rows
    output_grid.extend(non_black_rows)

    return np.array(output_grid).tolist()