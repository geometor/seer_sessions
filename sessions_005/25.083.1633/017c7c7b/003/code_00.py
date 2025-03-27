"""
1.  **Copy and Substitute:** Create a copy of the input grid. Substitute all blue (1) pixels with red (2) pixels in the copy.
2.  **Determine Output Height:** Calculate the output grid height. The output height should be greater than or equal to the input height. If the input height is even, the output height becomes the next largest odd number that allows for the padding pattern. If the input height is odd, the output height is increased by 2 (or until odd).
3.  **Create Extended Grid:** Create a new, empty grid with the determined output height and 3 columns. Fill all cells in the second column of this new grid with the value 2 (red).
4. **Copy to Extended Grid**: Populate the upper section of new grid with the values of the input grid.
5.  **Extend Pattern (Alternating 0 and 2 in the Third Column):** Fill the remaining cells in the third column by alternating between 0 and 2. Start this alternation by examining the *last row* of the *original input*. If the value in the third column is 0, the next should be 2. If it's 2, continue with 0. If it is anything else, continue with 0.
6.  **Final Output:** The extended grid now contains the complete transformed output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    
    # change output pixels 
    output_grid[output_grid == 1] = 2

    # extend height
    h = output_grid.shape[0]
    if h % 2 == 0:
        h += 3
        if (h-output_grid.shape[0])%2!=1:
            h -= 2
    else:
        h += 2

    new_output_grid = np.zeros((h, 3), dtype=int)
    new_output_grid[:,1] = 2

    for i in range(output_grid.shape[0]):
        new_output_grid[i,:] = output_grid[i,:]

    # Extend Pattern (Alternating 0 and 2 in the Third Column)
    last_val = 0 if input_grid.shape[0] == 0 else input_grid[input_grid.shape[0]-1, 2]
    if last_val==0:
        next_val = 2
    else:
        next_val = 0
    
    for i in range(input_grid.shape[0], h):
        new_output_grid[i, 2] = next_val
        next_val = 0 if next_val == 2 else 2  # Alternate between 0 and 2.

    return new_output_grid.tolist()