"""
1.  **Object Identification:** The input grid consists of alternating color columns, primarily magenta and another color (either white or black).

2.  **Column Expansion and Insertion:** Each original column is separated by a new column of azure (color 8).

3.  **Row Handling:**
    *   Each existing row is maintained.
    *    An azure (8) row is inserted between each original row
    *   The final row of the input is maintained.

4.  **Color Mapping**: The initial color in the input is kept in the expanded output. The second color alternates (see next rule).

5.  **Final Row Anomaly:** the final output row has a number of black (0) cells at the end, equal to the total number of black cells in the original input
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_cols = cols * 2  # Double the columns due to insertion
    output_rows = rows + rows -1 + 1 # original + inserted + copy of last row

    output_grid = np.full((output_rows, output_cols), 8, dtype=int)  # Initialize with azure

    # insert original rows with added azure column between original columns
    for i in range(rows):
        output_row_index = i * 2
        output_col_index = 0
        for j in range(cols):
           output_grid[output_row_index, output_col_index] = input_grid[i,j]
           output_col_index += 2 # skip the inserted azure column

    # copy the last row from input to output
    output_grid[output_rows-1, 0:output_cols:2] = input_grid[rows-1,:]

    # get black cell count in original input
    black_count = np.count_nonzero(input_grid == 0)

    # add black cells on the very last row.
    output_grid[output_rows-1, output_cols - black_count:] = 0

    return output_grid