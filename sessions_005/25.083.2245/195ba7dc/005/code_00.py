"""
Transforms an input grid into an output grid based on the presence of the digit '2' in each column. Columns with '2' are represented by a single column of all '1's in the output. Columns without '2' are processed together: their non-zero elements before any trailing zeros are counted, and this total count determines the combined width of these columns in the output. These non-zero elements are mapped to '1's in the output, while the rest are '0's.
"""

import numpy as np

def transform(input_grid):
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Separate columns with '2' and without '2'
    cols_with_2 = []
    cols_without_2 = []
    cols_without_2_indices = []
    for j in range(input_cols):
        col = [input_grid[i][j] for i in range(input_rows)]
        if 2 in col:
            cols_with_2.append(col)
        else:
            cols_without_2.append(col)
            cols_without_2_indices.append(j)

    # Calculate the width of the output section for columns without '2'
    output_width_no_2 = 0
    for col in cols_without_2:
        n = 0
        for i in range(input_rows):
            if col[i] != 0:
                n += 1
            else:
                if n > 0 :
                    break
        output_width_no_2 += n


    # Initialize output grid
    output_cols = len(cols_with_2) + output_width_no_2
    output_grid = [[0] * output_cols for _ in range(input_rows)]

    # Fill output columns for input columns with '2'
    output_col_index = 0
    for _ in cols_with_2:
        for i in range(input_rows):
            output_grid[i][output_col_index] = 1
        output_col_index += 1


    # Fill output columns for input columns without '2'
    output_col_sub_index = 0
    for col_index in range(len(cols_without_2)):
        col = cols_without_2[col_index]

        n = 0
        for i in range(input_rows):
          if col[i] != 0 :
            n += 1
          else:
            if n>0:
              break

        for i in range(n):
          output_grid[i][output_col_index + output_col_sub_index] = 1


        output_col_sub_index += n



    return output_grid