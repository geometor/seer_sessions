# 3af2c5a8 • 004 • example_1 • investigate_coder

---
```python
"""
The input grid is expanded to an output that is double in height and width. 
The azure pixels in the input are replicated in a specific pattern: 
the first and third columns are duplicated, and then the entire pattern 
is repeated to double the height.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid dimensions based on input grid size.
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows * 2
    output_cols = input_cols * 2

    output_grid = np.zeros((6, 8), dtype=int)
    
    # copy first col
    output_grid[:input_rows,0] = input_grid[:,0]
        
    # copy sec col
    output_grid[:input_rows,1] = input_grid[:,1]

    # copy and expand third col
    output_grid[:input_rows,2] = input_grid[:,2]
    output_grid[:input_rows,5] = input_grid[:,2]

    # copy forth col
    output_grid[:input_rows,3] = input_grid[:,3]
    
    # copy first row
    output_grid[3,:4] = output_grid[0,:4]
    output_grid[3,4:] = output_grid[0,4:]
        
    # copy sec row
    output_grid[4,:4] = output_grid[1,:4]
    output_grid[4,4:] = output_grid[1,4:]

    # copy third row
    output_grid[5,:4] = output_grid[2,:4]
    output_grid[5,4:] = output_grid[2,4:]

    return output_grid
```
