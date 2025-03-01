# e98196ab • 012 • refine_coder

---
```python
"""
The transformation removes the grey horizontal line, and removes all rows that contain only zeros. It combines the rows of other colored objects, keeping the objects in the same columns.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Remove grey (color 5)
    modified_grid = np.copy(input_grid)
    for r in range(rows):
        for c in range(cols):
            if modified_grid[r, c] == 5:
                modified_grid[r, c] = 0
    
    # Combine Rows, keeping colors in same columns
    output_row_index = 0
    for r in range(rows):
      row = modified_grid[r,:]
      is_zero = all(e == 0 for e in row) #check if entire row is zero
      if not is_zero:
        for c in range(cols):
          if modified_grid[r,c] != 0: #if cell not zero
            output_grid[output_row_index,c] = modified_grid[r,c] #copy color to output grid at same column

        output_row_index += 1

    #remove all zero rows, again
    output_grid_final=[]
    for i in range(output_grid.shape[0]):
      row = output_grid[i,:]
      is_zero = all(e == 0 for e in row) 
      if not is_zero:
        output_grid_final.append(list(row))
    output_grid_final = np.array(output_grid_final)

    return output_grid_final
```
