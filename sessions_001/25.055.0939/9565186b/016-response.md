# 9565186b • 016 • refine_coder

---
```python
"""
Identify the middle row of the input grid. Examine the pixels within the middle row. If the middle row contains *only* azure pixels, change all azure pixels in that row to gray. If the middle row contains azure pixels AND red or black pixels, DO NOT change the azure pixels.  All other pixels in the grid remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the number of rows in the grid
    rows = output_grid.shape[0]
    middle_row_index = rows // 2
    middle_row = output_grid[middle_row_index]

    # Check if the middle row contains only azure pixels (8)
    if np.all(middle_row == 8):
        output_grid[middle_row_index] = 5  # Change all to gray (5)
    #check for red(2) or black(0)    
    elif 2 in middle_row or 0 in middle_row:
       pass #do nothing
    elif 8 in middle_row:
        #if there is an 8, and we got here, it is a different condition not
        # covered yet, like a black underscore
        unique_colors = np.unique(middle_row)
        if 8 in unique_colors and (0 in unique_colors):
          pass #don't change the azure
        
    
    # Return the modified grid
    return output_grid
```
