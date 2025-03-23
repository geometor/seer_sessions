```python
"""
The transformation rule can be described as follows:

1.  **First Column Transformation:**
    *   If a value exists below the current value, copy it
    *   If a value exists in the last row of the first column, copy it
    *   Otherwise, the first column element remains unchanged.
2.  **Second Column Transformation**
    * If the first element of the second column is non-zero, copy that value down to all the rows of the second column
    *   If a value exists below a cell in the input, copy it
    *   Otherwise, do not change the value
3. **Third Column Transformation**
    *   If the first value is non-zero, copy it to all the cells in the third column
    *   Otherwise, do not change the value
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # First Column Transformation
    first_col_last_val = input_grid[-1,0]

    for i in range(rows):
        if i < rows - 1:
            output_grid[i+1,0] = input_grid[i,0] #copy from above
        elif first_col_last_val != 0 and i== rows-1:
             output_grid[i,0] = first_col_last_val


    # Second Column Transformation.
    first_val_second_col = input_grid[0,1]
    if (first_val_second_col != 0):
        for i in range(rows):
            output_grid[i, 1] = first_val_second_col
    elif rows > 2:
        for i in range(rows-1):
            output_grid[i+1,1] = input_grid[i,1]


    # Third Column Transformation
    first_val_third_col = input_grid[0,2]
    if(first_val_third_col != 0):
      for i in range(rows):
        output_grid[i,2] = first_val_third_col


    return output_grid
```