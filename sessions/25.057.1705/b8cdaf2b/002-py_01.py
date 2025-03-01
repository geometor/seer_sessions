"""
1.  **Identify the top row and bottom row of the input grid.**
2. **For each cell in top row**
   1.  **if the cell is not white(0)**
      1.  **do nothing**.
   2.  **if the cell is white(0)**
       1. **find the cell in the bottom row in same column**.
       2. **if the cell in the bottom row is 2(red)**
          1.   **Change the top row to yellow(4)**
       3. **if the cell in the bottom row is 4(yellow)**
          1.  **Change the top row to yellow (4)**
       4. **if cell in the bottom row is 0 (white)**
            1. **change the top row cell to a 0(white)**.
3.  **All other cells remain unchanged.**
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid)  # Initialize output as a copy of input
    num_rows = input_grid.shape[0]
    num_cols = input_grid.shape[1]

    # Iterate through each cell of top row
    for col in range(num_cols):

        #check it is white
        if output_grid[0, col] == 0:
            #find value in the bottom row same column
            bottom_row_val = input_grid[num_rows-1,col]
            #if 2 or 4 change to 4
            if bottom_row_val == 2 or bottom_row_val == 4:
                output_grid[0,col] = 4
            # output_grid[0, col] remains unchanged if it is not 0.

    return output_grid