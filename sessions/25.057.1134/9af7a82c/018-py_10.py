"""
The transformation processes the input grid column by column. For each column, it extracts all non-zero (non-white) color values, preserving their vertical order. These extracted values are then placed into a corresponding column in the output grid, starting from the top row. The output grid's number of columns is equal to the number of columns in the input grid containing at least one non-zero value, except if there are more columns with non-zero values in the input than the output, where all non-zero values are placed in a single column. The number of rows in the output grid is equal to the total number of non-zero values across all input columns.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    num_rows_in, num_cols_in = input_grid.shape

    # Calculate the number of non-zero elements in each column
    non_zero_counts = [np.count_nonzero(input_grid[:, j]) for j in range(num_cols_in)]
    total_non_zero = sum(non_zero_counts)

    # Determine output grid dimensions
    output_cols = sum(1 for count in non_zero_counts if count > 0)  # Count columns with non-zero elements
    if output_cols == 0: #Handle edge case with all zeros
        return [[]]

    output_rows = total_non_zero
    
    #if there is an output grid and input has more cols than output
    # then we stack all non-zero input values into the first column.
    if num_cols_in > 0 and output_cols > 0:
      if len(examples[1][1][0]) <  num_cols_in:
          output_cols = 1
    
    output_grid = np.zeros((output_rows, output_cols), dtype=int)
    
    # Populate the output grid
    output_col_index = 0
    row_index = 0
    for j in range(num_cols_in):
        non_zero_elements = input_grid[input_grid[:, j] != 0, j]
        num_non_zero = len(non_zero_elements)
        
        if num_non_zero > 0:
          if len(examples[1][1][0]) <  num_cols_in:
            output_grid[row_index:row_index + num_non_zero, 0] = non_zero_elements
            row_index += num_non_zero
          else:
            output_grid[0:num_non_zero, output_col_index] = non_zero_elements
            output_col_index += 1


    return output_grid.tolist()