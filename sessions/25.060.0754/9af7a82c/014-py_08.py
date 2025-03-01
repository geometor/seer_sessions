"""
1.  **Column Reversal:** The output grid's columns are a reversed sequence of the input grid's columns. Input column `i` becomes output column `width - 1 - i`.

2.  **Dynamic Height Adjustment:**
    *   Iterate through each column of input, comparing against the input grid.
    *    Prepend rows of color '0' above the current input column values until the colors in the current output grid do not exactly match the input grid.

3. **Column Value Transfer**
   * For each column in the input grid, transfer its values to the corresponding reversed column in the output grid, starting at an offset determined during dynamic height adjustment

4.  **No Trailing Fill:**  The output grid is *not* filled with the color of the last row.
"""

import numpy as np

def transform(input_grid):
    input_rows, input_cols = input_grid.shape
    output_grid = np.zeros((input_rows, input_cols), dtype=int)  # Initialize with the same size
    output_rows = 0


    # Column Value Transfer and Reversal
    for j in range(input_cols):
        output_col_index = input_cols - 1 - j
        output_grid[:, output_col_index] = input_grid[:, j]

    # Dynamic Height Adjustment and Column Value Transfer
    for j in range(input_cols):
        output_col_index = input_cols - 1 - j
        current_col = input_grid[:, j]
        
        prepended_rows = 0
        while True:
           
            temp_grid = np.zeros((input_rows + prepended_rows, input_cols), dtype=int)
            temp_grid[prepended_rows:, output_col_index] = current_col

            
            if prepended_rows > 0:
                
                is_match = True
                for col_check in range(input_cols):
                    if any(temp_grid[:input_rows,col_check] != input_grid[:,col_check]):
                        is_match = False
                        break

                if not is_match:
                  break

            prepended_rows += 1
            if (prepended_rows + input_rows) > 30:
                break


        if prepended_rows > output_rows:
          output_rows = prepended_rows + input_rows
          temp_output_grid = np.zeros((output_rows,input_cols), dtype = int)

          for cj in range(input_cols):
            output_col = input_cols - 1 - cj
            temp_output_grid[prepended_rows:,output_col] = input_grid[:,cj]
          output_grid = temp_output_grid
        else:
          output_grid[prepended_rows:,output_col_index] = input_grid[:,j]


    return output_grid