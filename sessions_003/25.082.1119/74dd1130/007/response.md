```python
"""
1.  **Column 2 Shift:** Copy the contents of the input grid's second column to the output grid's first column.
2.  **Column 3 Copy:** Copy the contents of the input grid's third column to the output grid's third column.
3.  **Column 1 Redistribution:** Copy the contents of the input's first column to the output, filling in the 2nd column, and then the third, top to bottom, left to right. The values in the input's first column should replace values in the output columns 2 and 3, if they had existing values as the result of a previous step.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Column 2 Shift: Move input's column 2 to output's column 1.
    output_grid[:, 0] = input_grid[:, 1]

    # 2. Column 3 Copy: Copy input's column 3 to output's column 3.
    output_grid[:, 2] = input_grid[:, 2]
    
    # 3. Column 1 Redistribution
    input_col1 = input_grid[:, 0]

    # fill available spots in the output_grid's second and third columns, overwriting existing values.
    k = 0
    for j in range(1,3): # Iterate through columns 2 and 3
       for i in range(output_grid.shape[0]):  # Iterate through rows            
            output_grid[i, j] = input_col1[k]
            k += 1
            if(k >= len(input_col1)):
              k = 0 # start over

    return output_grid
```