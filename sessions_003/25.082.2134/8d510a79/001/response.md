```python
"""
The transformation rule is as follows:
1.  Locate the row of grey (5) pixels. This row is copied unchanged to the output.
2.  Locate Action rows: Identify the rows that have blue or red colors.
3.  Duplicate: For any other color, copy the pixel, and add another pixel to it's right if a red or blue exits at that location to its right.
4.  Iterate: Perform steps 2, 3 for all rows in the Input and place them at the same index in Output.
5.  Double the height: Repeat the rows to double the overall height of the output.

In essence, select colored pixels are duplicated with some specific changes if they have blue or red neighbor to their right, and the entire grid's height is doubled by repeating each row.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 2, cols), dtype=int)

    # Iterate through each row of the input grid
    for i in range(rows):
        new_row = []
        for j in range(cols):
            # Copy the current pixel
            new_row.append(input_grid[i, j])
            
            # Check for blue (1) or red (2) to the right
            if j + 1 < cols and (input_grid[i, j+1] == 1 or input_grid[i, j+1] == 2) and (input_grid[i,j] == 1 or input_grid[i,j] == 2):
                new_row.append(input_grid[i,j])
        
        # Handle cases where duplication extends beyond original width. Truncate to maintain width.
        output_grid[i] = (new_row + [0]*cols)[:cols]  #pad and truncate.
        output_grid[i + rows] = (new_row+ [0]*cols)[:cols]

    return output_grid.tolist()
```