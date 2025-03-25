```python
"""
1. Column 2 Shift: Move the contents of the second column of the input grid to the first column of the output grid.
2. Column 3 Copy: Copy the contents of the third column of the input grid to the third column of the output grid.
3. Column 1 Redistribution: The contents of the first column from input grid are redistributed to fill the second and third columns in output grid. Each element will appear once, filling column positions that don't already contain the value from the operation of steps 1 and 2.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Column 2 Shift: Move input's column 2 to output's column 1.
    output_grid[:, 0] = input_grid[:, 1]

    # 2. Column 3 Copy: Copy input's column 3 to output's column 3.
    output_grid[:, 2] = input_grid[:, 2]
    
    # 3. Column 1 Redistribution
    input_col1 = input_grid[:, 0]
    redistributed = []
    
    #Iterate through input_col1 elements.
    for x in input_col1:
        if x not in redistributed:
            redistributed.append(x)

    # fill available spots in the output_grid
    k=0
    for i in range(output_grid.shape[0]):
        if output_grid[i,1] not in redistributed:
           output_grid[i,1] = redistributed[k]
           k += 1
           if(k >= len(redistributed)):
              k = 0 # start over

    return output_grid
```