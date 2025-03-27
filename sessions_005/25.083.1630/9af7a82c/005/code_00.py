"""
1.  **Input Reversal and Transposition:** Reverse the order of elements in *each* row of the input grid. The reversed elements from each row form the first column of the output. The element in the first column and first row of the input grid will begin the output grid.

2.  **Output Dimensions:**
    *   The output grid has the same number of columns as the input grid.
    *   The number of rows in the output grid is determined as follows:
        *   If the number of input rows is less than or equal to 5, the output has 5 rows.
        *   If the number of input rows is greater than 5, the output has 6 rows.

3. **Populate First Column:** The first column is created by reversing each input row, taking the last element, and placing them sequentially down the first column. The output will have as many elements in the first column as there are rows in the output.

4.  **Fill Remaining Cells:** Any remaining cells in the output grid (after placing the transposed elements) are filled with 0 (white). The reversed row elements, minus the last one (because they were used in the column), go into the output row.

5.  **First Row:** The first row in the output consists of: The element that was first in the input first column, followed by the rest of the reversed elements of the original first row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = 5 if rows <= 5 else 6
    output_grid = np.zeros((output_rows, cols), dtype=int)

    # populate first column of output
    first_col_elements = []
    for i in range(rows):
        first_col_elements.append(input_grid[i][-1])
    
    for i in range(output_rows):
        if i < len(first_col_elements):
            output_grid[i,0] = first_col_elements[i]

    # populate first row and other rows
    first_row_reversed = input_grid[0, :][::-1]
    output_grid[0, 0] = first_row_reversed[-1]

    for j in range(1,cols):
        if j < len(first_row_reversed):
          output_grid[0,j] = first_row_reversed[j-1]

    return output_grid